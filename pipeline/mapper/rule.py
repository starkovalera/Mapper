from .exceptions import *


class Rule:
    def __init__(self, keys_from, *args):
        self.keys_from, self.keys_to, self.transform_function = \
            self._resolve_arguments(keys_from, args)

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
            raise InvalidRuleConfigurationException(
                "Rule expected from 2 to 3 positional parameters: required 'keys from' "
                "and at least one of 'keys to', 'transform function'.\n"
                "Got: %s." % ', '.join(arg for arg in (keys_from, *args)))
        keys_from = self._handle_as_tuple(keys_from)
        if len(args) == 2:
            if not callable(args[1]):
                raise InvalidRuleConfigurationException(
                    "Rule expected from 2 to 3 positional parameters: required 'keys from' "
                    "and at least one of 'keys to', 'transform function'.\n'transform function' must be callable.\n"
                    "Got: %s." % ', '.join(arg for arg in (*keys_from, *args)))
            keys_to, transform_function = self._handle_as_tuple(args[0]), args[1]
        elif callable(args[0]):
            keys_to, transform_function = None, args[0]
        else:
            keys_to, transform_function = self._handle_as_tuple(args[0]), None
            if len(keys_to) != len(keys_from):
                raise InvalidRuleConfigurationException(
                    "Rule expected same number of 'keys from' and 'keys to' parameters if rule's"
                    " 'transform function' is None.\n Got 'keys from': %s; 'keys to': %s." %
                    (keys_from, keys_to))
        return keys_from, keys_to, transform_function

    @staticmethod
    def _handle_as_tuple(arg):
        return arg if isinstance(arg, tuple) else (arg,)
