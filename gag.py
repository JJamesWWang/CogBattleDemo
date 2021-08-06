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

