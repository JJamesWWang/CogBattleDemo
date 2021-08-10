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
        self.selectedGag: int = Gag.NONE
        self.selectedTarget: Combatant = None

    @overrides
    def executeAttack(self) -> None:
        if self.battle.cogs:
            target = random.choice(self.battle.cogs)
            target.takeDamage(Gag.DAMAGE[self.selectedGag])

    @overrides
    def isAttackHit(self) -> bool:
        rand = random.random()
        isHit = (
            True
            if self.isDeterministic
            else rand < 0.95 and rand < Gag.CHANCE_TO_HIT[self.selectedGag]
        )
        print(f"The toon {'hit' if isHit else 'missed'}")
        return isHit
