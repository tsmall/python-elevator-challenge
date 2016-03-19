from collections import namedtuple
import operator

import direction


UP = direction.UP
DOWN = direction.DOWN

Call = namedtuple('Call', ('floor', 'direction'))


def initial_state(num_floors):
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
    calls = [Call(floor, current_direction) for floor, called in enumerate(state[current_direction]) if called]
    comparator = operator.ge if current_direction == UP else operator.le
    possible = [call for call in calls if comparator(call.floor, current_floor)]
    return first(possible, None)


def _best_going_other_way(state, current_floor, current_direction):
    if current_direction == None:
        return None

    opposite_direction = direction.opposite(current_direction)
    if any(state[opposite_direction]):
        f = max if opposite_direction == DOWN else min
        floor = f(floor for floor, called in enumerate(state[opposite_direction]) if called)
        return Call(floor, opposite_direction)

    return None


def _nearest(state, current_floor):
    up_calls = [Call(floor, UP) for floor, called in enumerate(state[UP]) if called]
    down_calls = [Call(floor, DOWN) for floor, called in enumerate(state[DOWN]) if called]
    calls = up_calls + down_calls
    calls_with_distance = [(abs(call.floor - current_floor), call) for call in calls]
    nearest = first(sorted(calls_with_distance), (None, None))
    return nearest[1]


def call_serviced(state, (floor, direction)):
    """
    Record that the specified call has been serviced by an elevator.

    :param state: The current call state.
    :param call: The call that has been processed.
    :return: None
    """
    state[direction][floor] = False


def call_requested(state, floor, direction):
    state[direction][floor] = True


def first(iterable, default):
    for each in iterable:
        if each:
            return each
    return default
