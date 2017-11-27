class NullCallRequest(object):

    def when_serviced(self, action):
        # Intentionally don't do anything.
        None

    def tell_to_move(self, elevator):
        # Intentionally don't do anything.
        None

    def send_movement_direction_to(self, elevator, current_floor):
        # Intentionally don't do anything.
        None

    def floor_changed_to(self, new_floor):
        # Intentionally don't do anything.
        None
