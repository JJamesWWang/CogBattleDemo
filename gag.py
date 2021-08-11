"""Copyright 2021, James S. Wang, All rights reserved."""

from typing import List, Dict


class Gag:
    """Namespace containing all information about gags.

    Ideally, gag data would be read from a table, but here we have it hardcoded
    for simplicity.

    Attributes:
        NONE (int): A placeholder indicating that no gag is selected.
        PASS (int): The toon chooses to pass instead of selecting a gag.
        SQUIRT (int): Gag that does 4 damage with a 90% chance of hitting.
        THROW (int): Gag that does 6 damage with a 75% chance of hitting.
        DAMAGE (dict of int to int): Maps gags to damage.
        CHANCE_TO_HIT (dict of int to float): Maps gags to chance to hit.
        EXECUTE_ORDER (list of int): A sorted list of gags indicating order.
        TARGET_REQUIRED (list of int): A list of gags that require targets.
        NAME (dict of int to str): Maps gags to their names.
    """

    NONE: int = 0
    PASS: int = 1
    SQUIRT: int = 2
    THROW: int = 3
    DAMAGE: Dict[int, int] = {PASS: 0, SQUIRT: 4, THROW: 6}
    CHANCE_TO_HIT: Dict[int, float] = {PASS: 0.0, SQUIRT: 0.9, THROW: 0.75}
    EXECUTE_ORDER: List[int] = [SQUIRT, THROW]
    TARGET_REQUIRED: List[int] = [SQUIRT, THROW]
    NAME: Dict[int, str] = {
        PASS: "Pass",
        SQUIRT: "Squirt",
        THROW: "Throw",
    }
