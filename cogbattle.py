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
        self.gagSelectTimer = None
        self.timePrinter = TimePrinter()

    def enterGagSelect(self):
        print()
        print("Entered Gag Select")
        self.printStatus()
        self.gagSelectTimer = taskMgr.add(self.gagSelectTimerTick, 
                                          "GagSelectTimerTick")
        self.timePrinter.clear()

    def gagSelectTimerTick(self, task):
        if task.time > CogBattle.GAG_SELECT_WAIT_TIME:
            self.request(CogBattleState.GAG_EXECUTE)
            return Task.done
        self.timePrinter.printTime(
            int(CogBattle.GAG_SELECT_WAIT_TIME - task.time))
        return Task.cont

    def exitGagSelect(self):
        taskMgr.remove(self.gagSelectTimer)

    def enterGagExecute(self):
        cogs = self.battle.cogs
        self.executeGags(cogs)
        if cogs:
            self.demand(CogBattleState.COGS_ATTACK)
        else:
            self.demand(CogBattleState.TOONS_WON)

    def executeGags(self, cogs):
        for gag in sorted(self.battle.selectedGags):
            targetCog = 0
            if not Gag.isGagHit(gag):
                continue
            cogs[targetCog].takeDamage(Gag.DAMAGE[gag])
            if cogs[targetCog].isDead():
                cogs.pop(targetCog)

    def enterCogsAttack(self):
        toons = self.battle.toons
        self.executeCogAttacks(toons)
        if toons:
            self.demand(CogBattleState.GAG_SELECT)
        else:
            self.demand(CogBattleState.COGS_WON)

    def executeCogAttacks(self, toons):
        for cog in self.battle.cogs:
            attack = random.choice(Cog.ATTACKS)
            targetToon = 0
            if not Cog.isCogHit(attack):
                continue
            toons[targetToon].takeDamage(Cog.DAMAGE[attack])
            if toons[targetToon].isDead():
                toons.pop(targetToon)

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

    def startCogBattle(self):
        print("Starting Cog Battle")
        self.cogBattleFSM.request(CogBattleState.GAG_SELECT)

    def selectGag(self, gag):
        if self.cogBattleFSM.state != CogBattleState.GAG_SELECT:
            return
        print(f"Selected {gag}")
        self.selectedGags[0] = gag
        if all(self.selectedGags):
            self.startGagExecute()

    def startGagExecute(self):
        self.cogBattleFSM.request(CogBattleState.GAG_EXECUTE)

    def startCogsAttack(self):
        self.cogBattleFSM.request(CogBattleState.COGS_ATTACK)
