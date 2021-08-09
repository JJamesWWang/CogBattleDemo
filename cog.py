from combatant import Combatant
import random
from typing import List, Dict
from overrides import overrides


class Cog:
    def __init__(self):
        self.health = 12


class CogCombatant(Combatant):
    """Represents a cog, an AI combatant.

    Currently attacks, damage, and chance to hit are hardcoded; however,
    ideally these values would be read from a spreadsheet or filled through
    another more flexible method.
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
        pass

    def selectAttack(self) -> str:
        pass

    @overrides
    def isAttackHit(self) -> bool:
        isHit = (
            True
            if self.isDeterministic
            else random.random()
            < CogCombatant.CHANCE_TO_HIT[self.selectedAttack]
        )
        print(f"The cog {'hit' if isHit else 'missed'}")
        return isHit

    def isCogHit(self, cogAttack):
        self.selectedAttack = cogAttack
        return self.isAttackHit()
