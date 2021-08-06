import random


class Gag:
    NONE, PASS, SQUIRT, THROW = range(4)
    DAMAGE = {
        PASS: 0,
        SQUIRT: 4,
        THROW: 6
    }
    CHANCE_TO_HIT = {
        PASS: 0.0,
        SQUIRT: 0.9,
        THROW: 0.75
    }
    
    @staticmethod
    def isGagHit(gag) -> bool:
        rand = random.random()
        isHit = rand < 0.95 and rand < Gag.CHANCE_TO_HIT[gag]
        print(f"The toon {'hit' if isHit else 'missed'}")
        return isHit


