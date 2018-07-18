class Rule:
    def __init__(self, keys_from, keys_to=None, transform_function=None):
        self.keys_from = keys_from
        self.keys_to = keys_to
        self.transform_function = transform_function

    def execute(self, data):
        keys = self.keys_to if self.keys_to is not None else self.keys_from
        values = tuple(data.get(key) for key in self.keys_from)
        if self.transform_function is not None:
            values = self.transform_function(*values)
            if len(keys) == 1:
                values = values,
        data.update(zip(keys, values))