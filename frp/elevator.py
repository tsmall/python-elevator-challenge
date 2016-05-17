from collections import namedtuple
from frp.utils import *
from rx import Observable
from rx.subjects import BehaviorSubject, Subject


UP = 1
DOWN = 2
FLOOR_COUNT = 6


Call = namedtuple('Call', ('floor', 'direction'))


class Inputs(object):

    def __init__(self):
        self.called_S = Subject()
        self.floor_selected_S = Subject()
        self.floor_changed_S = Subject()
        self.tick_S = Subject()


class ElevatorLogic(object):

    def __init__(self):
        self.callbacks = None

        self._inputs = Inputs()
        motor_C = main(self._inputs, 1)
        motor_C.subscribe(self._set_motor)

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        self._inputs.called_S.on_next(Call(floor, direction))

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        self._inputs.floor_selected_S.on_next(floor)

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        self._inputs.floor_changed_S.on_next(self.callbacks.current_floor)

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        self._inputs.tick_S.on_next(None)

    def _set_motor(self, direction):
        """
        Set the motor to move in the specified direction, or to stop if the
        direction is None.
        """
        # This object's `callbacks` attribute isn't set until after it is
        # created. But our Rx streams will have fired once before then. So
        # check to make sure the attribute has been set before calling a
        # property on it.
        if self.callbacks is not None:
            self.callbacks.motor_direction = direction


def main(inputs, starting_floor):
    floor_C = BehaviorSubject(starting_floor)
    inputs.floor_changed_S.subscribe(floor_C)

    calls_C = BehaviorSubject(set())
    calls_S = inputs.called_S \
        .map(lambda call: call.floor) \
        .scan(lambda called_floors, floor: called_floors | set([floor]), set())
    calls_S.subscribe(calls_C)

    selections_C = BehaviorSubject(set())
    inputs.floor_selected_S \
        .scan(lambda selections, floor: selections | set([floor]), set()) \
        .subscribe(selections_C)

    resume_S = inputs.tick_S \
        .with_latest_from(selections_C, lambda _, selections: first(selections)) \
        .filter(cmp(not_, is_none))

    # TODO (TS 2016-05-16) Don't fire if motor is already moving.
    motor_started_S = inputs.called_S \
        .map(lambda call: call.floor) \
        .merge(inputs.floor_selected_S, resume_S) \
        .with_latest_from(floor_C, determine_direction)

    stop_for_call_S = inputs.floor_changed_S \
        .with_latest_from(calls_C, arrived_on_called_floor) \
        .filter(identity) \
        .map(always(None))

    stop_for_selection_S = inputs.floor_changed_S \
        .with_latest_from(selections_C, arrived_on_selected_floor) \
        .filter(identity) \
        .map(always(None))

    motor_stopped_S = Observable.merge(stop_for_call_S, stop_for_selection_S)

    motor_C = BehaviorSubject(None)
    motor_change_S = Observable.merge(motor_started_S, motor_stopped_S)
    motor_change_S.subscribe(motor_C)

    return motor_C


def arrived_on_called_floor(current_floor, called_floors):
    return current_floor in called_floors


def arrived_on_selected_floor(current_floor, selected_floors):
    return current_floor in selected_floors


def determine_direction(requested_floor, current_floor):
    return UP if requested_floor > current_floor else DOWN
