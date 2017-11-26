from direction import Direction
from floor import Floor
from request import CallRequest
from requestqueue import CallRequestQueue

class ElevatorLogic(object):
    """
    I represent the controller logic for an elevator.
    """

    def __init__(self):
        self.callbacks = None
        self._call_queue = CallRequestQueue(self)
        self._current_request = None

    @property
    def _current_floor(self):
        return Floor(self.callbacks.current_floor)

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the
        elevator. This could happen at any time, whether or not the elevator is
        moving. The elevator could be requested at any floor at any time, going
        in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        request = CallRequest(Floor(floor), Direction(direction))
        self._call_queue.add(request)

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor. This
        could happen at any time, whether or not the elevator is moving. Any
        floor could be requested at any time.

        floor: the floor that was requested
        """

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        self._current_request.floor_changed_to(self._current_floor)

    def on_ready(self):
        """
        This is called when the elevator is ready to go. Maybe passengers have
        embarked and disembarked. The doors are closed, time to actually move,
        if necessary.
        """
        self._call_queue.service_next_request()

    def begin_servicing_request(self, request):
        self._current_request = request
        request.when_serviced(self._request_serviced)
        request.send_movement_direction_to(self, self._current_floor)

    def _request_serviced(self, request):
        if request == self._current_request:
            self.stop()
            self._current_request = None

    def start_motor(self, raw_direction):
        self.callbacks.motor_direction = raw_direction

    def stop(self):
        self.callbacks.motor_direction = None
