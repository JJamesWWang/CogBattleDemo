from abc import ABC, abstractmethod


class Combatant(ABC):
    """The combatant is the base class for any character that will partake in
    battles.

    Attributes:
        health (int): How much health the combatant currently has.
    """

    def __init__(self):
        self.health: int

    def takeDamage(self, damage: int):
        """Tell this combatant to receive damage.

        The damage might not be equal to the passed in argument due to
        additional filtering or side effects.

        Args:
            damage (int)
        """
        self.health -= damage

    def isDead(self) -> bool:
        """Returns whether the combatant is dead."""
        return self.health <= 0
