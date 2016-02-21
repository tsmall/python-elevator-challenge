import calls

UP = 1
DOWN = 2


# Model ------------------------------------------------------------------------


def initial_elevator_state(num_floors):
    return {
        'current_direction': None,
        'requested_direction': None,
        'selected': [False] * (num_floors + 1),
        'calls': calls.initial_state(num_floors),
    }


# Actions ----------------------------------------------------------------------


def on_called(state, floor, direction):
    calls.call_requested(state['calls'], floor, direction)


def on_floor_selected(state, selected_floor, current_floor):
    if selected_floor == current_floor:
        return

    current_direction = _get_current_direction(state, current_floor)
    requested_direction = UP if selected_floor > current_floor else DOWN
    if current_direction in (requested_direction, None):
        state['selected'][selected_floor] = True
        state['current_direction'] = requested_direction
        state['requested_direction'] = None


def on_floor_changed(state, current_floor):
    assert current_floor < len(state['selected']), "Floor too large: {}".format(current_floor)
    assert current_floor > 0, "Floor below one: {}".format(current_floor)

    current_direction = _get_current_direction(state, current_floor)
    call = calls.available(state['calls'], current_floor, current_direction)

    if any(state['selected']):
        if state['selected'][current_floor]:
            state['current_direction'] = None
            state['selected'][current_floor] = False

        if call and call.floor == current_floor and call.direction == current_direction:
            state['current_direction'] = None
            state['requested_direction'] = call.direction
            calls.call_serviced(state['calls'], call)

    elif call and call.floor == current_floor:
        state['current_direction'] = None
        state['requested_direction'] = call.direction
        calls.call_serviced(state['calls'], call)


def on_ready(state, current_floor):
    current_direction = _get_current_direction(state, current_floor)
    call = calls.available(state['calls'], current_floor, current_direction)
    state['requested_direction'] = None

    if call and call.floor == current_floor and call.direction == current_direction:
        state['current_direction'] = None
        state['requested_direction'] = current_direction
        calls.call_serviced(state['calls'], call)

    elif any(state['selected']):
        state['current_direction'] = current_direction
        state['requested_direction'] = None

    elif call:
        if call.floor == current_floor:
            state['current_direction'] = None
            state['requested_direction'] = call.direction
            calls.call_serviced(state['calls'], call)

        elif call:
            state['current_direction'] = UP if call.floor > current_floor else DOWN
            state['requested_direction'] = None


# Utils ------------------------------------------------------------------------


def _get_current_direction(state, current_floor):
    return state['current_direction'] \
        or state['requested_direction'] \
        or _get_floor_direction(state, current_floor)


def _get_floor_direction(state, current_floor):
    floor_direction = None
    if any(state['selected']):
        floor = _get_next_floor(state['selected'])
        floor_direction = UP if floor > current_floor else DOWN
    return floor_direction


def _get_next_floor(bool_list):
    return next(floor for floor, called in enumerate(bool_list) if called)
