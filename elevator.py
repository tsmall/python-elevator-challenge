UP = 1
DOWN = 2
FLOOR_COUNT = 6

class ElevatorLogic(object):

    def __init__(self):
        self.callbacks = None
        self.requests = set()

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        if self.callbacks.motor_direction in (None, direction):
            self.requests.add(floor)

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        self.requests.add(floor)

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        if self.callbacks.current_floor in self.requests:
            self.callbacks.motor_direction = None

        self.requests.discard(self.callbacks.current_floor)

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        if not self.requests:
            return

        requested_floor = min(self.requests)
        if requested_floor > self.callbacks.current_floor:
            self.callbacks.motor_direction = UP
        elif requested_floor < self.callbacks.current_floor:
            self.callbacks.motor_direction = DOWN
