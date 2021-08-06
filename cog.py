import random


class Cog:
    ATTACK_A = "Attack A"
    ATTACK_B = "Attack B"

    def __init__(self):
        self.health = 12
        self.attacks = [self.ATTACK_A, self.ATTACK_B]
        self.damage = {
            self.ATTACK_A: 2,
            self.ATTACK_B: 3
        }

    def takeDamage(self, damage):
        self.health -= damage

    def isDead(self):
        return self.health <= 0

    def executeAttack(self):
        attack = random.choice(self.attacks)
