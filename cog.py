import random


class Cog:
    ATTACK_A = "Attack A"
    ATTACK_B = "Attack B"
    ATTACKS = [ATTACK_A, ATTACK_B]
    DAMAGE = {
        ATTACK_A: 2,
        ATTACK_B: 3
    }
    CHANCE_TO_HIT = {
        ATTACK_A: 0.85,
        ATTACK_B: 0.6
    }

    def __init__(self):
        self.health = 12

    def takeDamage(self, damage):
        self.health -= damage

    def isDead(self):
        return self.health <= 0

    @staticmethod
    def isCogHit(cogAttack):
        isHit = random.random() < Cog.CHANCE_TO_HIT[cogAttack]
        print(f"The cog {'hit' if isHit else 'missed'}")
        return isHit
