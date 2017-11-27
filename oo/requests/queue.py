from oo.list import SmartList
from null import NullCallRequest

class RequestQueue(object):
    """
    I represent the queue of requests passengers have made.
    """

    def __init__(self, elevator):
        self._elevator = elevator
        self._requests = SmartList()

    def add_call_request(self, request):
        self._requests.insert(0, request)

    def add_selection_request(self, request):
        self._requests.append(request)

    def _remove(self, request):
        if request in self._requests:
            self._requests.remove(request)

    def service_next_request(self):
        self._with_next_request_do(self._service_request)

    def _with_next_request_do(self, action):
        self._requests.with_first_or_default_do(
            default=NullCallRequest(),
            action=action
        )

    def _service_request(self, request):
        request.when_serviced(self._remove)
        request.tell_to_move(self._elevator)
