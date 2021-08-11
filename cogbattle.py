"""Copyright 2021, James S. Wang, All rights reserved."""

from combatant import Combatant
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
    """Namespace for the different states possible in the CogBattleFSM"""

    GAG_SELECT: str = "GagSelect"
    GAG_EXECUTE: str = "GagExecute"
    COGS_ATTACK: str = "CogsAttack"
    TOONS_WON: str = "ToonsWon"
    COGS_WON: str = "CogsWon"


class CogBattleFSM(FSM):
    """The finite state-machine representing a cog battle's state.

    Args:
        name (str): The name to provide the finite state-machine.
        battle (CogBattle): The CogBattle that this FSM belongs to.

    Attributes:
        state (str): The current state that the FSM is in.
        defaultTransitions (dict of str to list of str): The valid transitions
            from state to state.
        battle (CogBattle): The CogBattle that this FSM belongs to.
        gagSelectTimer (Task): The task that runs the gag select timer.
        timePrinter (TimePrinter): Util object to print the gag select timer.
    """

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
        for toon in self.battle.toons:
            toon.selectedGag = Gag.NONE
            toon.selectedTarget = None

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
        """Adds all of the pending toons and cogs to their respective lists."""
        self.battle.toons.extend(self.battle.pendingToons)
        self.battle.pendingToons = []
        self.battle.cogs.extend(self.battle.pendingCogs)
        self.battle.pendingCogs = []
        self.printStatus()

    def resetGagSelectTimer(self) -> None:
        """Resets the gag select timer back to its starting time."""
        taskMgr.remove(self.gagSelectTimer)
        self.gagSelectTimer = taskMgr.add(
            self.gagSelectTimerTick, "GagSelectTimerTick"
        )
        self.timePrinter.clear()

    def exitGagSelect(self) -> None:
        taskMgr.remove(self.gagSelectTimer)

    def enterGagExecute(self) -> None:
        self.battle.executeGags()
        if self.battle.cogs or self.battle.pendingCogs:
            self.demand(CogBattleState.COGS_ATTACK)
        else:
            self.demand(CogBattleState.TOONS_WON)

    def enterCogsAttack(self) -> None:
        self.battle.attackToons()
        if self.battle.toons or self.battle.pendingToons:
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
        """Prints all toons and cogs in the cog battle."""
        for i, toon in enumerate(self.battle.toons):
            print(f"Toon {i + 1}: {toon.health} laff")
        for i, cog in enumerate(self.battle.cogs):
            print(f"Cog {i + 1}: {cog.health} health")
        print()


class CogBattle:
    """Represents a cog battle.

    Args:
        toons (list of Toon): The toons that initiated this battle.
        cogs (list of Cog): The cogs that initiated this battle.
        deterministic (bool): Whether the battle's outcomes should be
            deterministic.

    Attributes:
        GAG_SELECT_WAIT_TIME (int): How long to wait during gag select.
        MAX_TOONS_IN_BATTLE (int): How many toons can join the battle.
        MAX_COGS_IN_BATTLE (int): How many cogs can join the battle.
        toons (list of ToonCombatant): All toon combatants in the battle.
        cogs (list of CogCombatant): All cog combatants in the battle.
        isDeterminstic (bool): Whether the battle's outcomes are deterministic.
        cogBattleFSM (CogBattleFSM): The finite state-machine that represents
            this cog battle's state.
        pendingToons (list of ToonCombatant): Toons waiting to join the battle.
        pendingCogs (list of CogCombatant): Cogs waiting to join the battle.
        selectedGagTurn (int): The index of the toon to select a gag for.
    """

    GAG_SELECT_WAIT_TIME: int = 10
    MAX_TOONS_IN_BATTLE: int = 4
    MAX_COGS_IN_BATTLE: int = 4

    def __init__(
        self, toons: List[Toon], cogs: List[Cog], deterministic: bool = False
    ) -> None:
        self.toons = [
            ToonCombatant(self, toon, deterministic) for toon in toons
        ]
        self.cogs = [CogCombatant(self, cog, deterministic) for cog in cogs]
        self.isDeterministic = deterministic
        self.cogBattleFSM: CogBattleFSM = CogBattleFSM("CogBattleFSM", self)
        self.pendingToons: List[ToonCombatant] = []
        self.pendingCogs: List[CogCombatant] = []
        self.selectedGagTurn: int = 0

    def startCogBattle(self) -> None:
        """Requests the cog battle to start."""
        print("Starting Cog Battle")
        if self.cogBattleFSM.state == "Off":
            self.cogBattleFSM.request(CogBattleState.GAG_SELECT)

    def selectGag(self, gag: int) -> None:
        """Selects a gag for the next toon.

        Args:
            gag (int): One of the constants in the Gag class.
        """
        if self.cogBattleFSM.state != CogBattleState.GAG_SELECT:
            return
        print(
            f"Selected {gag} for toon {self.selectedGagTurn + 1}, "
            "select a cog next."
        )
        self.toons[self.selectedGagTurn].selectedGag = gag
        if len(self.cogs) == 1 or gag not in Gag.TARGET_REQUIRED:
            self.selectTarget(0)

    def selectTarget(self, target: int) -> None:
        """Selects a target cog for the next toon.

        Args:
            target (int): An index in the cogs list.
        """
        if self.cogBattleFSM.state != CogBattleState.GAG_SELECT:
            return
        if target >= len(self.cogs):
            print("Selected nonexistent cog, try again")
            return

        print(f"Selected cog {target + 1}")
        self.toons[self.selectedGagTurn].selectedTarget = self.cogs[target]
        self.selectedGagTurn = (self.selectedGagTurn + 1) % len(self.toons)
        if all(toon.selectedGag for toon in self.toons):
            self.cogBattleFSM.request(CogBattleState.GAG_EXECUTE)

    def executeGags(self) -> None:
        """Commits all gags selected by toons."""
        for gag in Gag.EXECUTE_ORDER:
            attackingToons = [
                toon for toon in self.toons if toon.selectedGag == gag
            ]
            # Use the first toon to roll for a hit; if the first succeeds, so
            # do the rest.
            if attackingToons and attackingToons[0].isAttackHit():
                for toon in attackingToons:
                    toon.executeAttack()
                self.cogs = [cog for cog in self.cogs if cog.isAlive()]

    def attackToons(self) -> None:
        """Tells all cogs to execute an attack on the toons."""
        for cog in self.cogs:
            if cog.isAttackHit():
                cog.executeAttack()
        self.toons = [toon for toon in self.toons if toon.isAlive()]

    def requestToonJoin(self, toon: Toon) -> None:
        """Requests for a toon to join the battle.

        Args:
            toon (Toon): The toon that wants to join the battle.
        """
        if len(self.toons) + len(self.pendingToons) < self.MAX_TOONS_IN_BATTLE:
            print("Adding Toon")
            self.pendingToons.append(
                ToonCombatant(self, toon, self.isDeterministic)
            )

    def requestCogJoin(self, cog: Cog) -> None:
        """Requests for a cog to join the battle.

        Args:
            cog (Cog): The cog that wants to join the battle.
        """
        if len(self.cogs) + len(self.pendingCogs) < self.MAX_COGS_IN_BATTLE:
            print("Adding Cog")
            self.pendingCogs.append(
                CogCombatant(self, cog, self.isDeterministic)
            )
