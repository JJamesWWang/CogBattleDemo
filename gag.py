from typing import List, Dict


class Gag:
    NONE: int = 0
    PASS: int = 1
    SQUIRT: int = 2
    THROW: int = 3
    DAMAGE: Dict[int, int] = {PASS: 0, SQUIRT: 4, THROW: 6}
    CHANCE_TO_HIT: Dict[int, float] = {PASS: 0.0, SQUIRT: 0.9, THROW: 0.75}
    EXECUTE_ORDER: List[int] = [SQUIRT, THROW]
    TARGET_REQUIRED: List[int] = [SQUIRT, THROW]
