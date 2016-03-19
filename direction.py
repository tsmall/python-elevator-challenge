UP = 1
DOWN = 2


def opposite(direction):
    assert(direction in (UP, DOWN))
    return DOWN if direction == UP else UP
