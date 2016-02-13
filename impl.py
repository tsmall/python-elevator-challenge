UP = 1
DOWN = 2


# Model ------------------------------------------------------------------------


def make_elevator_struct(floor_count):
    return {
        'current_direction': None,
        'requested_direction': None,
        'selected': _make_floor_list(floor_count),
        'calls': {
            UP: _make_floor_list(floor_count),
            DOWN: _make_floor_list(floor_count),
            None: _make_floor_list(floor_count),
        },
    }


def _make_floor_list(floor_count):
    return [False] * (floor_count + 1)


# Actions ----------------------------------------------------------------------


def on_called(struct, floor, direction):
    struct['calls'][direction][floor] = True


def on_floor_selected(struct, selected_floor, current_floor):
    if selected_floor == current_floor:
        return

    current_direction = _get_current_direction(struct, current_floor)
    requested_direction = UP if selected_floor > current_floor else DOWN
    if current_direction in (requested_direction, None):
        struct['selected'][selected_floor] = True
        struct['current_direction'] = requested_direction


def on_floor_changed(struct, current_floor):
    current_direction = _get_current_direction(struct, current_floor)
    opposite_direction = _get_opposite_direction(current_direction)

    if any(struct['calls'][current_direction]) or any(struct['selected']):
        if struct['calls'][current_direction][current_floor]:
            struct['requested_direction'] = current_direction
            struct['current_direction'] = None
            struct['calls'][current_direction][current_floor] = False

        if struct['selected'][current_floor]:
            struct['current_direction'] = None
            struct['selected'][current_floor] = False

    elif struct['calls'][opposite_direction][current_floor]:
        struct['current_direction'] = None
        struct['requested_direction'] = opposite_direction
        struct['calls'][opposite_direction][current_floor] = False


def on_ready(struct, current_floor):
    current_direction = _get_current_direction(struct, current_floor)
    opposite_direction = _get_opposite_direction(current_direction)

    if any(struct['calls'][current_direction]) or any(struct['selected']):
        struct['current_direction'] = current_direction
        struct['requested_direction'] = None

    elif opposite_direction is not None and any(struct['calls'][opposite_direction]):
        floor = _get_next_floor(struct['calls'][opposite_direction])
        if floor == current_floor:
            struct['requested_direction'] = opposite_direction
            struct['calls'][DOWN][floor] = False
        else:
            struct['current_direction'] = UP if floor > current_floor else DOWN
            struct['requested_direction'] = None

    else:
        struct['requested_direction'] = None
        if any(struct['calls'][UP]):
            floor = _get_next_floor(struct['calls'][UP])
            struct['current_direction'] = UP if floor > current_floor else DOWN
            if floor == current_floor:
                struct['calls'][UP][floor] = False
        elif any(struct['calls'][DOWN]):
            floor = _get_next_floor(struct['calls'][DOWN])
            struct['current_direction'] = UP if floor > current_floor else DOWN
            if floor == current_floor:
                struct['calls'][DOWN][floor] = False


# Helpers ----------------------------------------------------------------------


def _get_current_direction(struct, current_floor):
    floor_direction = None
    if any(struct['selected']):
        floor = _get_next_floor(struct['selected'])
        floor_direction = UP if floor > current_floor else DOWN

    return struct['current_direction'] or struct['requested_direction'] or floor_direction


def _get_opposite_direction(direction):
    opposites = {
        UP: DOWN,
        DOWN: UP,
        None: None,
    }
    return opposites[direction]


def _get_next_floor(bool_list):
    return next(floor for floor, called in enumerate(bool_list) if called)
