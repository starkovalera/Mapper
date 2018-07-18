from itertools import chain
from django.db import transaction
from .exceptions import *


class DjangoModelWriter:
    def __init__(self, model_class, only_write_to=None, not_write_to=None):
        if only_write_to is not None and not_write_to is not None:
            raise InvalidWriterConfigurationException("Only one of 'only_write_to', 'not_write_to' parameters must "
                                                      "be supplied.")
        self._model_class = model_class
        self._fields = self._filter_model_fields(only_write_to, not_write_to)

    def write(self, data_set):
        with transaction.atomic():
            self._model_class.objects.bulk_create([self._model_class(**self._filter_data(item)) for item in data_set])

    def _filter_data(self, data):
        return {field: data[field] for field in self._fields}

    def _filter_model_fields(self, only_write_to, not_write_to):
        model_fields = self._get_model_fields()
        if only_write_to is not None:
            model_fields &= set(only_write_to)
        if not_write_to is not None:
            model_fields -= set(not_write_to)
        if not model_fields:
            raise InvalidWriterConfigurationException("Resulting field set is empty.")
        return model_fields

    def _get_model_fields(self):
        return set(chain.from_iterable(
            (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
            for field in self._model_class._meta.get_fields() if not (field.many_to_one and field.related_model is None)
        ))
