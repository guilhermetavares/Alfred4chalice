from unittest.mock import Mock

from alfred.sqlalchemy_utils.filters.schemas import FilterSchema
from alfred.auth.models import BasicAuthUser
from marshmallow import Schema


def test_filter_schema_parent_class():
    assert issubclass(FilterSchema, Schema) is True


def test_filter_schema_build_filter_commom_filter():
    username = BasicAuthUser(username="Esquilo")
    BasicAuthUser(username="Unicórnio")

    query = Mock()

    data = {
        "username": {
            "model": BasicAuthUser,
            "field_name": "username",
            "op": "==",
            "value": "Esquilo",
            "filter_type": "sqlalchemy.and_",
        }
    }

    schema = FilterSchema(query=query)
    filtered_mock_query = schema.make_object(data)

    filtered_mock_query.one() == username

# testes