class CallRequest(object):
    """
    I represent a single call request made by a passenger, consisting of both
    the floor they made the request from and the direction they requested to go
    when they get on the elevator.
    """

    def __init__(self, floor, direction):
        self._serviced_actions = []
        self._floor = floor
        self._direction = direction

    def when_serviced(self, action):
        self._serviced_actions.append(action)

    def tell_to_move(self, elevator):
        elevator.begin_servicing_request(self)

    def send_movement_direction_to(self, elevator, current_floor):
        current_floor.send_direction_to_floor(
            self._floor,
            lambda direction: self._send_direction(elevator, direction)
        )

    def _send_direction(self, elevator, direction):
        direction.send_raw_value_to(
            lambda raw_direction: elevator.start_motor(raw_direction)
        )

    def floor_changed_to(self, new_floor):
        self._floor.on_match(new_floor, self._serviced)

    def _serviced(self):
        for action in self._serviced_actions:
            action(self)


class NullCallRequest(object):

    def when_serviced(self, action):
        # Intentionally don't do anything.
        None

    def tell_to_move(self, elevator):
        # Intentionally don't do anything.
        None

    def send_movement_direction_to(self, elevator, current_floor):
        # Intentionally don't do anything.
        None

    def floor_changed_to(self, new_floor):
        # Intentionally don't do anything.
        None
