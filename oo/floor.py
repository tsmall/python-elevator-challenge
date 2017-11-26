from direction import Direction

class Floor(object):
    """
    I represent a single floor in a building.
    """

    def __init__(self, floor_number):
        self._number = floor_number

    def on_match(self, other_floor, action):
        other_floor._if_equal(self._number, action)

    def _if_equal(self, floor_number, action):
        if self._number == floor_number:
            action()

    def send_direction_to(self, other_floor, action):
        other_floor._if_above(self._number, lambda: action(Direction.UP))
        other_floor._if_below(self._number, lambda: action(Direction.DOWN))

    def _if_above(self, floor_number, action):
        if floor_number < self._number:
            action()

    def _if_below(self, floor_number, action):
        if floor_number > self._number:
            action()
