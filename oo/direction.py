class Direction(object):
    """
    I represent a direction the elevator can move.
    """

    def __init__(self, raw_value):
        self._raw_value = raw_value

    def send_raw_value_to(self, action):
        action(self._raw_value)

Direction.UP = Direction(1)
Direction.DOWN = Direction(2)
