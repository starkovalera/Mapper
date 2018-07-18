from .rule import Rule


class Mapper:
    """Applies transformation rules to single unit of data."""

    def __init__(self, transform_map):
        """
        :param transform_map: (:obj:`tuple` of :obj:`tuple`): Each inner tuple corresponds to one transformation rule
        and contains from 2 to 3 parameters for rule creation.
        """
        self._transform_map = self._build_transform_map(transform_map)

    def map(self, data):
        if self._transform_map:
            for rule in self._transform_map:
                rule.execute(data)
        return data

    @staticmethod
    def _build_transform_map(transform_map):
        return tuple(Rule(*rule) for rule in transform_map)

