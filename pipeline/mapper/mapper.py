from .rule import Rule


class Mapper:
    def __init__(self, transform_map):
        self._transform_map = self._build_transform_map(transform_map)

    def map(self, data):
        if self._transform_map:
            for rule in self._transform_map:
                rule.execute(data)
        return data

    @staticmethod
    def _build_transform_map(transform_map):
        return tuple(Rule(*rule) for rule in transform_map)

