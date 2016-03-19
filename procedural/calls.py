from collections import namedtuple
import operator
import time

import direction


UP = direction.UP
DOWN = direction.DOWN

Call = namedtuple('Call', ('floor', 'direction'))


def initial_state(num_floors):
    # The requests are stored as a list. The list's size is one larger than the
    # number of floors, so the list's indexes match the floor numbers. The
    # values can either be False, indicating the floor doesn't have a request,
    # or a timestamp of the time the request was made.
    make_list = lambda: [False] * (num_floors + 1)
    return {
        UP: make_list(),
        DOWN: make_list(),
        None: make_list(),
    }


def available(state, current_floor, current_direction):
    """
    Find the next available call, taking into consideration the elevator's
    current direction and which floor it is on.

    :param state: The current call state.
    :param current_floor: The floor the elevator is on.
    :param current_direction: The direction the elevator is moving.
    :return: The next available call, or None.
    """
    tests = (
        _on_floor_going_right_way(state, current_floor, current_direction),
        _next_going_right_way(state, current_floor, current_direction),
        _best_going_other_way(state, current_floor, current_direction),
        _nearest(state, current_floor),
    )
    return first(tests, None)


def _on_floor_going_right_way(state, current_floor, current_direction):
    if state[current_direction][current_floor]:
        return Call(current_floor, current_direction)
    return None


def _next_going_right_way(state, current_floor, current_direction):
    calls = _call_list(state, current_direction)
    comparator = operator.ge if current_direction == UP else operator.le
    possible = [call for call in calls if comparator(call.floor, current_floor)]
    return first(possible, None)


def _best_going_other_way(state, current_floor, current_direction):
    if current_direction == None:
        return None

    opposite_direction = direction.opposite(current_direction)
    if any(state[opposite_direction]):
        f = max if opposite_direction == DOWN else min
        return f(_call_list(state, opposite_direction))

    return None


def _nearest(state, current_floor):
    calls_with_time = _call_list_with_times(state, UP) + _call_list_with_times(state, DOWN)
    calls_with_distance_and_time = [
        (abs(call.floor - current_floor), time_called, call)
        for time_called, call in calls_with_time
    ]

    distance, time_called, call = first(
        sorted(calls_with_distance_and_time),
        (None, None, None),
    )
    return call


def _call_list(state, direction):
    return [call for time_called, call in _call_list_with_times(state, direction)]


def _call_list_with_times(state, direction):
    return [
        (time_called, Call(floor, direction))
        for floor, time_called in enumerate(state[direction])
        if time_called
    ]


def call_serviced(state, (floor, direction)):
    """
    Record that the specified call has been serviced by an elevator.

    :param state: The current call state.
    :param call: The call that has been processed.
    :return: None
    """
    state[direction][floor] = False


def call_requested(
        state,
        current_floor, requested_floor,
        is_stopped, current_direction, requested_direction
):
    on_floor = (current_floor == requested_floor)
    going_that_way = (current_direction == requested_direction)
    if is_stopped and on_floor and going_that_way:
        return

    state[requested_direction][requested_floor] = time.time()


def first(iterable, default):
    for each in iterable:
        if each:
            return each
    return default
