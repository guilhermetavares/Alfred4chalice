from unittest.mock import Mock
from sqlalchemy import or_
from alfred.sqlalchemy_utils.filters.operators import OPERATORS

from alfred.sqlalchemy_utils.filters.schemas import FilterSchema
from marshmallow import Schema


def test_filter_schema_parent_class():
    assert issubclass(FilterSchema, Schema) is True


def test_filter_schema_build_filter_commom_filter():
    model = Mock()
    query = Mock()
    operator = OPERATORS["=="]

    data = {
        "username": {
            "model": model,
            "field_name": "username",
            "op": "==",
            "value": "Esquilo",
            "filter_type": "sqlalchemy.and_",
        }
    }
    expected_operator = operator("username", "Esquilo")
    expected_query = query.filter(expected_operator)

    schema = FilterSchema(query=query)
    filtered_query = schema.make_object(data)

    assert filtered_query == expected_query


def test_filter_schema_build_filter_logical_filter():
    model = Mock()
    query = Mock()
    operator = OPERATORS["=="]

    data = {
        "username": {
            "model": model,
            "field_name": "username",
            "op": "==",
            "value": "Esquilo",
            "filter_type": "sqlalchemy.or_",
        }
    }

    expected_operator = or_(operator("username", "Esquilo"))
    expected_query = query.filter(expected_operator)

    schema = FilterSchema(query=query)
    filtered_query = schema.make_object(data)

    assert filtered_query == expected_query
