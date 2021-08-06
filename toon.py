class Toon:
    def __init__(self) -> None:
        self.laff: int = 15

    def takeDamage(self, damage: int) -> None:
        self.laff -= damage

    def isDead(self) -> bool:
        return self.laff <= 0
