from combatant import Combatant
from gag import Gag
from typing import List
from overrides import overrides
import random


class Toon:
    def __init__(self):
        self.laff = 15


class ToonCombatant(Combatant):
    """Represents a player's toon."""

    def __init__(
        self, battle: "CogBattle", toon: Toon, deterministic: bool = False
    ) -> None:
        super().__init__(battle, deterministic)
        self.health = toon.laff
        self.selectedGag = Gag.NONE

    @overrides
    def executeAttack(self) -> None:
        pass

    @overrides
    def isAttackHit(self) -> bool:
        rand = random.random()
        isHit = rand < 0.95 and rand < Gag.CHANCE_TO_HIT[self.selectedGag]
        print(f"The toon {'hit' if isHit else 'missed'}")
        return isHit
