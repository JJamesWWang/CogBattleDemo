from combatant import Combatant
import random
from typing import List, Dict
from overrides import overrides


class Cog(Combatant):
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

    def __init__(self, deterministic: bool = False) -> None:
        self.health: int = 12
        self.isDeterministic: bool = deterministic

    @overrides
    def executeAttack(self, targets: List[Combatant]):
        pass

    def isCogHit(self, cogAttack: str) -> bool:
        isHit = (
            True
            if self.isDeterministic
            else random.random() < Cog.CHANCE_TO_HIT[cogAttack]
        )
        print(f"The cog {'hit' if isHit else 'missed'}")
        return isHit
