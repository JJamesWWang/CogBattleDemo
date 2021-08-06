import random
from typing import Dict


class Gag:
    NONE: int = 0
    PASS: int = 1 
    SQUIRT: int = 2
    THROW: int = 3
    DAMAGE: Dict[int, int] = {
        PASS: 0,
        SQUIRT: 4,
        THROW: 6
    }
    CHANCE_TO_HIT: Dict[int, float] = {
        PASS: 0.0,
        SQUIRT: 0.9,
        THROW: 0.75
    }
    
    @staticmethod
    def isGagHit(gag: int) -> bool:
        rand = random.random()
        isHit = rand < 0.95 and rand < Gag.CHANCE_TO_HIT[gag]
        print(f"The toon {'hit' if isHit else 'missed'}")
        return isHit


