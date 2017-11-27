class SelectionRequest(object):

    def __init__(self, floor):
        self._floor = floor
        self._on_serviced_actions = []

    def when_serviced(self, action):
        self._on_serviced_actions.append(action)

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
        for action in self._on_serviced_actions:
            action(self)
