"""Copyright 2021, James S. Wang, All rights reserved."""

from combatant import Combatant
from gag import Gag
from typing import List
from overrides import overrides
import random


class Toon:
    """Represents a toon as it would in the normal gameplay mode.

    The idea here is to separate battle logic from non-battle logic by creating
    new objects when battles are initiated.

    Attributes:
        laff (int): Hardcoded health of the toon is set to 15. Ideally, we
            would track the toon's laff, gag level, experience, etc.
    """

    def __init__(self):
        self.laff = 15


class ToonCombatant(Combatant):
    """Represents a player's toon in combat.

    Args:
        battle (CogBattle): The CogBattle that instantiates this toon.
        toon (Toon): The toon to base this combatant off of.
        deterministic (bool): Whether the combatant's actions are
            deterministic. Used for unit testing.

    Attributes:
        selectedGag (int): One of the constants in the Gag class; used to
            determine which gag is used when executing an attack.
        selectedTarget (Combatant): A target for the selectedGag, if necessary.
    """

    def __init__(
        self, battle: "CogBattle", toon: Toon, deterministic: bool = False
    ) -> None:
        super().__init__(battle, deterministic)
        self.health = toon.laff
        self.selectedGag: int = Gag.NONE
        self.selectedTarget: Combatant = None

    @overrides
    def executeAttack(self) -> None:
        if self.battle.cogs and self.selectedTarget.isAlive():
            self.selectedTarget.takeDamage(Gag.DAMAGE[self.selectedGag])

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
