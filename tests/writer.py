import pytest
from unittest.mock import Mock
from pipeline.writer.writer import DjangoModelWriter
from pipeline.writer.exceptions import *


class MockModelField:
    def __init__(self, name):
        self.name = name
        self.many_to_one = False


def create_mock_model(field_number=4):
    model = Mock()
    model._meta.get_fields = Mock(return_value=[MockModelField('field' + str(i)) for i in range(field_number)])
    model.object.bulk_create = Mock(return_value=None)
    return model


class TestDjangoModelWriter:
    def test_fields_only_write_to(self):
        model = create_mock_model()
        writer = DjangoModelWriter(model, only_write_to=('field1', 'field3'))
        assert writer._fields == {'field1', 'field3'}

    def test_fields_not_write_to(self):
        model = create_mock_model()
        writer = DjangoModelWriter(model, not_write_to=('field1', 'field3'))
        assert writer._fields == {'field0', 'field2'}

    def test_only_write_to_and_not_write_to(self):
        model = create_mock_model()
        with pytest.raises(InvalidWriterConfigurationException):
            DjangoModelWriter(model, only_write_to=('field1', 'field3'), not_write_to=('field0',))

    def test_empty_resulting_fields(self):
        model = create_mock_model()
        with pytest.raises(InvalidWriterConfigurationException):
            DjangoModelWriter(model, not_write_to=('field0', 'field1', 'field2', 'field3'))




