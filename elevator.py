import operator

UP = 1
DOWN = 2
FLOOR_COUNT = 6

class ElevatorLogic(object):

    def __init__(self):
        self.callbacks = None

        self.pending_stops = set()  # Pending stops in the direction we're going.
        self.queued_requests = []   # Requests to answer when we change directions.
        self.resume_dir = None      # Direction to continue after stopping on a floor.

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        going_the_right_way = self.current_direction == direction
        if going_the_right_way and not self.already_passed(floor):
            self.pending_stops.add((floor, direction))
        else:
            self.queued_requests.append((floor, direction))

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        if floor == self.callbacks.current_floor:
            return

        requested_direction = UP if floor > self.callbacks.current_floor else DOWN

        if requested_direction == self.current_direction:
            self.pending_stops.add((floor, requested_direction))

        if self.current_direction is None:
            self.pending_stops.add((floor, requested_direction))
            self.go(requested_direction)

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        get_next_stop = min if self.current_direction == UP else max
        floor, direction = stop = get_next_stop(self.pending_stops)
        if floor == self.callbacks.current_floor:
            self.stop()
            self.resume_dir = direction
            self.pending_stops.remove(stop)

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        if self.resume_dir is not None:
            if self.pending_stops:
                self.go(self.resume_dir)
            self.resume_dir = None

        if self.queued_requests:
            requests = self.queued_requests
            self.queued_requests = []

            first, rest = requests[0], requests[1:]

            floor, direction = first
            if floor == self.callbacks.current_floor:
                self.resume_dir = direction
            else:
                self.pending_stops.add((floor, direction))
                self.go(UP if floor > self.callbacks.current_floor else DOWN)

            for floor, direction in rest:
                self.on_called(floor, direction)

    @property
    def current_direction(self):
        return self.callbacks.motor_direction or self.resume_dir

    def already_passed(self, floor):
        test_for = {
            UP: operator.le,
            DOWN: operator.ge,
            None: lambda _: False,
        }
        return test_for[self.current_direction](floor, self.callbacks.current_floor)

    def go(self, direction):
        self.callbacks.motor_direction = direction

    def stop(self):
        self.callbacks.motor_direction = None
