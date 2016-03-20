from collections import namedtuple
from rx import Observable
from rx.subjects import BehaviorSubject, Subject


UP = 1
DOWN = 2
FLOOR_COUNT = 6


Call = namedtuple('Call', ('floor', 'direction'))


class ElevatorLogic(object):

    def __init__(self):
        self.callbacks = None

        self.inputs = {
            'called': Subject(),
            'floor_selected': Subject(),
            'floor_changed': Subject(),
            'ready': Subject(),
        }

        current_direction = main(self.inputs)
        current_direction.subscribe(lambda direction: self._go(direction))

    def _go(self, direction):
        self.callbacks.motor_direction = direction

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        self.inputs['called'].on_next((floor, direction))

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        self.inputs['floor_selected'].on_next(floor)

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        self.inputs['floor_changed'].on_next(self.callbacks.current_floor)

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        self.inputs['ready'].on_next(None)


def main(inputs):
    # A stream loop for the outstanding calls.
    s_calls = Subject()

    current_floor = BehaviorSubject(1)
    inputs['floor_changed'].subscribe(current_floor)

    s_new_calls = _create_new_calls(inputs['called'])
    s_serviced_calls = _create_serviced_calls(current_floor, s_calls) \
        .publish().ref_count()

    _create_calls(s_new_calls, s_serviced_calls).subscribe(s_calls)

    s_direction_changes = _create_direction_changes(
        inputs['ready'],
        s_serviced_calls,
        s_calls,
        current_floor
    )

    return s_direction_changes.publish().ref_count()


def _create_new_calls(s_called):
    return s_called \
        .map(lambda (floor, direction): Call(floor, direction))


def _create_serviced_calls(current_floor, s_calls):
    return current_floor \
        .with_latest_from(s_calls, find_call_on_floor) \
        .filter(bool)


def _create_calls(s_new_calls, s_serviced_calls):
    call_mod_fns = Observable.merge(
        s_new_calls.map(lambda call: list_adder(call)),
        s_serviced_calls.map(lambda call: list_remover(call))
    )
    return call_mod_fns \
        .scan(lambda calls, fn: fn(calls), seed=[])


def _create_direction_changes(s_ready, s_serviced_calls, s_calls, current_floor):
    s_starts = s_ready \
        .with_latest_from(s_calls, lambda _, calls: find_next_call(calls)) \
        .filter(bool) \
        .with_latest_from(current_floor, lambda call, floor: UP if floor < call.floor else DOWN)

    s_stops = s_serviced_calls \
        .map(lambda call: None)

    return Observable.merge(s_starts, s_stops)


def find_next_call(calls):
    return first(calls, None)


def find_call_on_floor(floor, calls):
    matching_calls = [call for call in calls if call.floor == floor]
    return first(matching_calls, None)


def list_adder(item):
    def adder(lst):
        return lst + [item]
    return adder


def list_remover(item):
    def remover(lst):
        return [each for each in lst if each != item]
    return remover


def first(lst, default):
    return lst[0] if lst else default
