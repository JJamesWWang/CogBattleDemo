from combatant import Combatant


class Toon(Combatant):
    """Represents a player's toon."""

    def __init__(self) -> None:
        self.health = 15
