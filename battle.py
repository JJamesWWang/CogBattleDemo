from combatant import Combatant
from typing import List


class Battle:
    def __init__(self, sides: List[List[Combatant]]):
        self.sides: List[List[Combatant]] = sides
        self.turn: int = 0

    def advanceTurn(self) -> None:
        actingSide = self.sides[self.turn]
        for combatant in actingSide:
            if combatant.isAttackHit():
                combatant.executeAttack()
            self.clearDeadCombatants()
        self.turn = (self.turn + 1) % len(self.sides)

    def clearDeadCombatants(self):
        for i, side in enumerate(self.sides):
            self.sides[i] = [
                combatant for combatant in side if not combatant.isDead()
            ]
