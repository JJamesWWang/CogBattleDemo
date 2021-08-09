from combatant import Combatant
from typing import List
from overrides import overrides


class Toon(Combatant):
    """Represents a player's toon."""

    def __init__(self) -> None:
        self.health = 15

    @overrides
    def executeAttack(self, targets: List[Combatant]) -> None:
        pass
