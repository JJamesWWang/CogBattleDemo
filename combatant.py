"""Copyright 2021, James S. Wang, All rights reserved."""

from abc import ABC, abstractmethod
from overrides import EnforceOverrides


class Combatant(ABC, EnforceOverrides):
    """The combatant is the base class for any character that will partake in
    battles.

    The idea here is to separate battle logic from non-battle logic by creating
    new objects (combatants) when battles are initiated.

    Args:
        battle (CogBattle): The battle that this combatant is a part of.
        deterministic (bool): Whether the combatant's actions are
            deterministic.

    Attributes:
        health (int): How much health the combatant currently has.
        battle (CogBattle): The battle that this combatant is a part of.
        isDeterministic (bool): Whether the combatant's actions are
            deterministic.
    """

    def __init__(self, battle: "CogBattle", deterministic: bool = False):
        self.health: int
        self.battle: "CogBattle" = battle
        self.isDeterministic: bool = deterministic

    @abstractmethod
    def executeAttack(self) -> None:
        """Tell this combatant to execute its attack."""

    @abstractmethod
    def isAttackHit(self) -> bool:
        """Returns whether the combatant's next attack will hit."""

    def takeDamage(self, damage: int) -> None:
        """Tell this combatant to receive damage.

        The damage might not be equal to the passed in argument due to
        additional filtering or side effects.

        Args:
            damage (int): Pre-filtered damage to receive.
        """
        self.health -= damage

    def isAlive(self) -> bool:
        """Returns whether the combatant is alive."""
        return self.health > 0
