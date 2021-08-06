class Toon:
    def __init__(self):
        self.laff = 15

    def takeDamage(self, damage):
        self.laff -= damage

    def isDead(self) -> bool:
        return self.laff <= 0
