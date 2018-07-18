import pytest
from operator import neg, mul
from math import modf
from pipeline.mapper.rule import Rule
from pipeline.mapper.exceptions import *


class TestRuleCreation:
    def test_empty_args(self):
        with pytest.raises(InvalidRuleConfigurationException):
            Rule('key_from')

    def test_two_args_without_callable(self):
        with pytest.raises(InvalidRuleConfigurationException):
            Rule('key_from', 'keys_to', 'not_callable')

    def test_two_args_with_callable(self):
        rule = Rule('key_from', 'key_to', neg)
        assert rule.keys_from == ('key_from',)
        assert rule.keys_to == ('key_to',)
        assert rule.transform_function is neg

    def test_keys_as_single_values(self):
        rule = Rule('key_from', 'key_to')
        assert rule.keys_from == ('key_from',)
        assert rule.keys_to == ('key_to',)
        assert rule.transform_function is None

    def test_keys_as_tuples(self):
        rule = Rule(('key_from1', 'key_from2'), ('key_to1', 'key_to2'))
        assert rule.keys_from == ('key_from1', 'key_from2')
        assert rule.keys_to == ('key_to1', 'key_to2')
        assert rule.transform_function is None

    def test_keys_as_different_length_tuples(self):
        with pytest.raises(InvalidRuleConfigurationException):
            Rule(('key_from1', 'key_from2', 'key_from3'), ('key_to1', 'key_to2'))

    def test_keys_as_tuple_and_single_value(self):
        with pytest.raises(InvalidRuleConfigurationException):
            Rule('key_from', ('key_to1', 'key_to2'))

    def test_with_transform_function_only(self):
        rule = Rule(('key_from1', 'key_from2'), divmod)
        assert rule.keys_from == ('key_from1', 'key_from2')
        assert rule.keys_to is None
        assert rule.transform_function is divmod


class TestRuleExecution:
    def test_execute_without_transform_functions_and_keys_as_single_values(self):
        rule = Rule('key_from', 'key_to')
        data = {'key_from': 1}
        rule.execute(data)
        assert data == {'key_from': 1, 'key_to': 1}

    def test_execute_without_transform_functions_and_keys_as_tuples(self):
        rule = Rule(('key_from1', 'key_from2'), ('key_to1', 'key_to2'))
        data = {'key_from1': 1, 'key_from2': 2}
        rule.execute(data)
        assert data == {'key_from1': 1, 'key_from2': 2, 'key_to1': 1, 'key_to2': 2}

    def test_execute_with_transform_functions_and_keys_as_single_values(self):
        rule = Rule('key_from', 'key_to', neg)
        data = {'key_from': 2}
        rule.execute(data)
        assert data == {'key_from': 2, 'key_to': neg(data.get('key_from'))}

    def test_execute_with_transform_functions_and_keys_as_tuples(self):
        rule = Rule(('key_from1', 'key_from2'), ('key_to1', 'key_to2'), divmod)
        data = {'key_from1': 2, 'key_from2': 3}
        rule.execute(data)
        val_to1, val_to2 = divmod(data.get('key_from1'), data.get('key_from2'))
        assert data == {'key_from1': 2, 'key_from2': 3, 'key_to1': val_to1,
                        'key_to2': val_to2}

    def test_execute_with_transform_function_tuple_to_single_value(self):
        rule = Rule(('key_from1', 'key_from2'), 'key_to', mul)
        data = {'key_from1': 2, 'key_from2': 3}
        rule.execute(data)
        assert data == {'key_from1': 2, 'key_from2': 3, 'key_to': mul(data.get('key_from1'), data.get('key_from2'))}

    def test_execute_with_transform_functions_single_value_to_tuple(self):
        rule = Rule('key_from', ('key_to1', 'key_to2'), modf)
        data = {'key_from': 2.5}
        rule.execute(data)
        val_to1, val_to2 = modf(data.get('key_from'))
        assert data == {'key_from': 2.5, 'key_to1': val_to1, 'key_to2': val_to2}










