"""Copyright 2021, James S. Wang, All rights reserved."""

from combatant import Combatant
import random
from typing import List, Dict
from overrides import overrides


class Cog:
    """Represents a cog as it would in the normal gameplay mode.

    Attributes:
        health (int): Hardcoded health of the cog is set to 12. Ideally, we
            would pass in the cog's suit and level to the constructor and
            health would automatically be determined according to some table.
    """

    def __init__(self) -> None:
        self.health: int = 12


class CogCombatant(Combatant):
    """Represents a cog, an AI combatant.

    Currently attacks, damage, and chance to hit are hardcoded; however,
    ideally these values would be read from a spreadsheet or filled through
    another more flexible method.

    Args:
        battle (CogBattle): The CogBattle that instantiates this cog.
        cog (Cog): The cog to base this combatant off of.
        deterministic (bool): Whether the combatant's actions are
            deterministic. Used for unit testing.

    Attributes:
        ATTACK_A (str): Generic attack 1.
        ATTACK_B (str): Generic attack 2.
        ATTACKS (list of str): All attacks this cog can execute.
        DAMAGE (dict of str to int): Damage of each attack.
        CHANCE_TO_HIT (dict of str to float): Chance of each attack hitting,
            from 0 to 1.
        selectedAttack (str): The attack to use when executing an attack.
    """

    ATTACK_A: str = "Attack A"
    ATTACK_B: str = "Attack B"
    ATTACKS: List[str] = [ATTACK_A, ATTACK_B]
    DAMAGE: Dict[str, int] = {ATTACK_A: 2, ATTACK_B: 3}
    CHANCE_TO_HIT: Dict[str, float] = {ATTACK_A: 0.85, ATTACK_B: 0.6}

    def __init__(
        self, battle: "CogBattle", cog: Cog, deterministic: bool = False
    ) -> None:
        super().__init__(battle, deterministic)
        self.health: int = cog.health
        self.selectedAttack: str = self.ATTACK_A

    @overrides
    def executeAttack(self):
        if self.battle.toons:
            self.selectAttack()
            target = (
                self.battle.toons[0]
                if self.isDeterministic
                else random.choice(self.battle.toons)
            )
            target.takeDamage(self.DAMAGE[self.selectedAttack])

    def selectAttack(self) -> None:
        """Sets the selectedAttack attribute to a random attack, or the first
        one if this combatant is set to be deterministic."""
        self.selectedAttack = (
            self.ATTACKS[0]
            if self.isDeterministic
            else random.choice(self.ATTACKS)
        )

    @overrides
    def isAttackHit(self) -> bool:
        self.selectAttack()
        isHit = (
            True
            if self.isDeterministic
            else random.random()
            < CogCombatant.CHANCE_TO_HIT[self.selectedAttack]
        )
        print(f"The cog {'hit' if isHit else 'missed'}")
        return isHit
