from request import NullCallRequest

class CallRequestQueue(object):
    """
    I represent the queue of call requests that passengers have made.
    """

    def __init__(self, elevator):
        self._elevator = elevator
        self._next_request = NullCallRequest()

    def add(self, request):
        self._next_request = request

    def _remove(self, request):
        if request == self._next_request:
            self._next_request = NullCallRequest()

    def service_next_request(self):
        self._next_request.when_serviced(self._remove)
        self._next_request.tell_to_move(self._elevator)
