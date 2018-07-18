from .exceptions import *


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

    def _resolve_arguments(self, keys_from, args):
        if not args or len(args) > 2:
            raise InvalidRuleConfigurationException()
        keys_from = self._handle_as_tuple(keys_from)
        if len(args) == 2:
            if not callable(args[1]):
                raise InvalidRuleConfigurationException()
            keys_to, transform_function = self._handle_as_tuple(args[0]), args[1]
        elif callable(args[0]):
            keys_to, transform_function = None, args[0]
        else:
            keys_to, transform_function = self._handle_as_tuple(args[0]), None
            if len(keys_to) != len(keys_from):
                raise InvalidRuleConfigurationException()
        return keys_from, keys_to, transform_function

    @staticmethod
    def _handle_as_tuple(arg):
        return arg if isinstance(arg, tuple) else (arg,)
