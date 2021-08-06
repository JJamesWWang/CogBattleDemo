from direct.fsm.FSM import FSM
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from gag import Gag
from cog import Cog
from toon import Toon
from utils import TimePrinter
import random


class CogBattleState:
    GAG_SELECT = "GagSelect"
    GAG_EXECUTE = "GagExecute"
    COGS_ATTACK = "CogsAttack"
    TOONS_WON = "ToonsWon"
    COGS_WON = "CogsWon"


class CogBattleFSM(FSM):
    def __init__(self, name, battle):
        super().__init__(name)
        self.defaultTransitions = {
            CogBattleState.GAG_SELECT: [CogBattleState.GAG_EXECUTE],
            CogBattleState.GAG_EXECUTE: [CogBattleState.COGS_ATTACK, 
                                         CogBattleState.TOONS_WON],
            CogBattleState.COGS_ATTACK: [CogBattleState.GAG_SELECT, 
                                         CogBattleState.COGS_WON],
            CogBattleState.TOONS_WON: [],
            CogBattleState.COGS_WON: []
        }
        self.battle = battle

    def enterGagSelect(self):
        print("Entered Gag Select")
        self.printStatus()

    def exitGagSelect(self):
        print("Exited Gag Select")

    def enterGagExecute(self):
        print("Entered Gag Execute")

    def exitGagExecute(self):
        print("Exited Gag Execute")

    def enterCogsAttack(self):
        print("Entered Cogs Attack")

    def exitCogsAttack(self):
        print("Exited Cogs Attack")

    def enterCogsWon(self):
        print("Cogs won the battle!")
        self.printStatus()

    def enterToonsWon(self):
        print("Toons won the battle!")
        self.printStatus()

    def printStatus(self):
        for i, toon in enumerate(self.battle.toons):
            print(f"Toon {i + 1}: {toon.laff} laff")
        for i, cog in enumerate(self.battle.cogs):
            print(f"Cog {i + 1}: {cog.health} health")
        print()


class CogBattle:
    GAG_SELECT_WAIT_TIME = 10
    MAX_TOONS_IN_BATTLE = 1
    MAX_COGS_IN_BATTLE = 1

    def __init__(self, cog):
        self.cogBattleFSM = CogBattleFSM("CogBattleFSM", self)
        self.toons = [Toon()]
        self.cogs = [cog]
        self.selectedGags = [Gag.PASS] * len(self.toons)
        self.gagSelectTimer = None
        self.timePrinter = TimePrinter()

    def startCogBattle(self):
        print("Starting Cog Battle")
        self.startGagSelect()

    def startGagSelect(self):
        if not self.cogBattleFSM.request(CogBattleState.GAG_SELECT):
            return
        self.gagSelectTimer = taskMgr.add(self.gagSelectTimerTick, 
                                          "GagSelectTimerTick")
        self.timePrinter.clear()

    def gagSelectTimerTick(self, task):
        if task.time > self.GAG_SELECT_WAIT_TIME:
            self.handleGagSelectEnded()
            return Task.done
        self.timePrinter.printTime(int(self.GAG_SELECT_WAIT_TIME - task.time))
        return Task.cont

    def selectGag(self, gag):
        if self.cogBattleFSM.state != CogBattleState.GAG_SELECT:
            return
        print(f"Selected {gag}")
        self.selectedGags[0] = gag
        if all(self.selectedGags):
            self.executeGags()

    def handleGagSelectEnded(self):
        self.executeGags()

    def executeGags(self):
        if not self.cogBattleFSM.request(CogBattleState.GAG_EXECUTE):
            return
        taskMgr.remove(self.gagSelectTimer)

        self.selectedGags.sort()
        for gag in self.selectedGags:
            targetCog = 0
            if not self.isGagHit(gag):
                continue
            self.cogs[targetCog].takeDamage(Gag.DAMAGE[gag])
            if self.cogs[targetCog].isDead():
                self.cogs.pop(targetCog)

        if self.cogs:
            self.cogsAttack()
        else:
            self.endBattle(True)

    def isGagHit(self, gag) -> bool:
        rand = random.random()
        isHit = rand < 0.95 and rand < Gag.CHANCE_TO_HIT[gag]
        print(f"The toon {'hit' if isHit else 'missed'}")
        return isHit

    def cogsAttack(self):
        if not self.cogBattleFSM.request(CogBattleState.COGS_ATTACK):
            return
        for cog in self.cogs:
            attack = random.choice(Cog.ATTACKS)
            targetToon = 0
            if not self.isCogHit(attack):
                continue
            self.toons[targetToon].takeDamage(Cog.DAMAGE[attack])
            if self.toons[targetToon].isDead():
                self.toons.pop(targetToon)

        if self.toons:
            self.startGagSelect()
        else:
            self.endBattle(False)

    def isCogHit(self, cogAttack):
        isHit = random.random() < Cog.CHANCE_TO_HIT[cogAttack]
        print(f"The cog {'hit' if isHit else 'missed'}")
        return isHit

    def endBattle(self, isToonWin: bool):
        if isToonWin:
            self.cogBattleFSM.request(CogBattleState.TOONS_WON)
        else:
            self.cogBattleFSM.request(CogBattleState.COGS_WON)
