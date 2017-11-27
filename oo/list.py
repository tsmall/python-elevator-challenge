class SmartList(list):
    """
    I represent a list of items.
    I'm like the normal Python list (`[]`),
    only smarter.
    """

    def with_first_or_default_do(self, default, action):
        item = self._get(0, default)
        action(item)

    def _get(self, index, default=None):
        try:
            return self[index]
        except:
            return default
