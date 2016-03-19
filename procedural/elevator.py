import impl

FLOOR_COUNT = 6

class ElevatorLogic(object):

    def __init__(self):
        self.callbacks = None
        self.data = impl.initial_elevator_state(FLOOR_COUNT)

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        impl.on_called(self.data, floor, direction, self.callbacks.current_floor)

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        impl.on_floor_selected(self.data, floor, self.callbacks.current_floor)
        self.go(self.data['current_direction'])

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        impl.on_floor_changed(self.data, self.callbacks.current_floor)
        self.go(self.data['current_direction'])

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        impl.on_ready(self.data, self.callbacks.current_floor)
        self.go(self.data['current_direction'])

    def go(self, direction):
        self.callbacks.motor_direction = direction
