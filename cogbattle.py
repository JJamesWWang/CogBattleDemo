from battle import Battle
from cog import Cog, CogCombatant
from direct.fsm.FSM import FSM
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from gag import Gag
from toon import Toon, ToonCombatant
from typing import Dict, List
from utils import TimePrinter
import random


class CogBattleState:
    GAG_SELECT: str = "GagSelect"
    GAG_EXECUTE: str = "GagExecute"
    COGS_ATTACK: str = "CogsAttack"
    TOONS_WON: str = "ToonsWon"
    COGS_WON: str = "CogsWon"


class CogBattleFSM(FSM):
    def __init__(self, name: str, battle: "CogBattle"):
        super().__init__(name)
        self.defaultTransitions: Dict[str, List[str]] = {
            CogBattleState.GAG_SELECT: [CogBattleState.GAG_EXECUTE],
            CogBattleState.GAG_EXECUTE: [
                CogBattleState.COGS_ATTACK,
                CogBattleState.TOONS_WON,
            ],
            CogBattleState.COGS_ATTACK: [
                CogBattleState.GAG_SELECT,
                CogBattleState.COGS_WON,
            ],
            CogBattleState.TOONS_WON: [],
            CogBattleState.COGS_WON: [],
        }
        self.battle: CogBattle = battle
        self.gagSelectTimer: Task = None
        self.timePrinter: TimePrinter = TimePrinter()

    def enterGagSelect(self) -> None:
        print()
        print("Entered Gag Select")
        self.printStatus()
        self.gagSelectTimer = taskMgr.add(
            self.gagSelectTimerTick, "GagSelectTimerTick"
        )
        self.timePrinter.clear()
        self.battle.selectedGagTurn = 0

    def gagSelectTimerTick(self, task: Task) -> int:
        if (
            len(self.battle.pendingToons) > 0
            or len(self.battle.pendingCogs) > 0
        ):
            self.addPendingCombatants()
            return self.resetGagSelectTimer()

        if task.time > CogBattle.GAG_SELECT_WAIT_TIME:
            self.request(CogBattleState.GAG_EXECUTE)
            return Task.done
        self.timePrinter.printTime(
            int(CogBattle.GAG_SELECT_WAIT_TIME - task.time)
        )
        return Task.cont

    def addPendingCombatants(self) -> None:
        self.battle.toons.extend(self.battle.pendingToons)
        self.battle.pendingToons = []
        self.battle.cogs.extend(self.battle.pendingCogs)
        self.battle.pendingCogs = []
        self.printStatus()

    def resetGagSelectTimer(self) -> None:
        taskMgr.remove(self.gagSelectTimer)
        self.gagSelectTimer = taskMgr.add(
            self.gagSelectTimerTick, "GagSelectTimerTick"
        )

    def exitGagSelect(self) -> None:
        taskMgr.remove(self.gagSelectTimer)

    def enterGagExecute(self) -> None:
        self.battle.advanceTurn()
        if self.battle.cogs:
            self.demand(CogBattleState.COGS_ATTACK)
        else:
            self.demand(CogBattleState.TOONS_WON)

    def enterCogsAttack(self) -> None:
        self.battle.advanceTurn()
        if self.battle.toons:
            self.demand(CogBattleState.GAG_SELECT)
        else:
            self.demand(CogBattleState.COGS_WON)

    def enterCogsWon(self) -> None:
        print("Cogs won the battle!")
        self.printStatus()

    def enterToonsWon(self) -> None:
        print("Toons won the battle!")
        self.printStatus()

    def printStatus(self) -> None:
        for i, toon in enumerate(self.battle.toons):
            print(f"Toon {i + 1}: {toon.health} laff")
        for i, cog in enumerate(self.battle.cogs):
            print(f"Cog {i + 1}: {cog.health} health")
        print()


class CogBattle(Battle):
    GAG_SELECT_WAIT_TIME: int = 10
    MAX_TOONS_IN_BATTLE: int = 4
    MAX_COGS_IN_BATTLE: int = 4

    def __init__(
        self, toons: List[Toon], cogs: List[Cog], deterministic: bool = False
    ) -> None:
        toons = [ToonCombatant(self, toon, deterministic) for toon in toons]
        cogs = [CogCombatant(self, cog, deterministic) for cog in cogs]
        super().__init__([toons, cogs])
        self.isDeterministic = deterministic
        self.cogBattleFSM: CogBattleFSM = CogBattleFSM("CogBattleFSM", self)
        self.pendingToons: List[Toon] = []
        self.pendingCogs: List[Cog] = []
        self.selectedGagTurn = 0

    @property
    def toons(self):
        return self.sides[0]

    @property
    def cogs(self):
        return self.sides[1]

    def startCogBattle(self) -> None:
        print("Starting Cog Battle")
        self.cogBattleFSM.request(CogBattleState.GAG_SELECT)

    def selectGag(self, gag: int) -> None:
        if self.cogBattleFSM.state != CogBattleState.GAG_SELECT:
            return
        print(f"Selected {gag} for toon {self.selectedGagTurn + 1}")
        self.toons[self.selectedGagTurn].selectedGag = gag
        self.selectedGagTurn = (self.selectedGagTurn + 1) % len(self.toons)
        if all(toon.selectedGag for toon in self.toons):
            self.cogBattleFSM.request(CogBattleState.GAG_EXECUTE)

    def requestToonJoin(self, toon: Toon) -> None:
        if len(self.toons) + len(self.pendingToons) < self.MAX_TOONS_IN_BATTLE:
            print("Adding Toon")
            self.pendingToons.append(
                ToonCombatant(self, toon, self.isDeterministic)
            )

    def requestCogJoin(self, cog: Cog) -> None:
        if len(self.cogs) + len(self.pendingCogs) < self.MAX_COGS_IN_BATTLE:
            print("Adding Cog")
            self.pendingCogs.append(
                CogCombatant(self, cog, self.isDeterministic)
            )
