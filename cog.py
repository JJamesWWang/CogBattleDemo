import random
from typing import List, Dict


class Cog:
    ATTACK_A: str = "Attack A"
    ATTACK_B: str = "Attack B"
    ATTACKS: List[str] = [ATTACK_A, ATTACK_B]
    DAMAGE: Dict[str, int] = {
        ATTACK_A: 2,
        ATTACK_B: 3
    }
    CHANCE_TO_HIT: Dict[str, float] = {
        ATTACK_A: 0.85,
        ATTACK_B: 0.6
    }

    def __init__(self) -> None:
        self.health: int = 12

    def takeDamage(self, damage: int) -> None:
        self.health -= damage

    def isDead(self) -> bool:
        return self.health <= 0

    @staticmethod
    def isCogHit(cogAttack: str) -> bool:
        isHit = random.random() < Cog.CHANCE_TO_HIT[cogAttack]
        print(f"The cog {'hit' if isHit else 'missed'}")
        return isHit
