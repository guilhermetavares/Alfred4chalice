import datetime

from alfred.sqlalchemy_utils.filters.fields import DateFilterField, StringFilterField
from alfred.auth.models import BasicAuthUser
from marshmallow import fields


def test_stringfilter_is_subclass():
    assert issubclass(StringFilterField, fields.String)


def test_stringfilter_success():
    field = StringFilterField(model=BasicAuthUser, op="==")
    document = "12309845687"

    value = field._deserialize(document, "document", {"document": document})

    assert value == {
        "model": BasicAuthUser,
        "field_name": "document",
        "filter_type": "sqlalchemy.and_",
        "op": "==",
        "value": "12309845687",
    }


def test_datefilter_is_subclass():
    assert issubclass(DateFilterField, fields.Date)


def test_datefilter_success():
    field = DateFilterField(
        model=BasicAuthUser,
        field_name="created_at",
        op=">=",
    )
    created_at_start = "2022-05-10"

    value = field._deserialize(
        created_at_start, "created_at_start", {"created_at_start": created_at_start}
    )

    assert value == {
        "model": BasicAuthUser,
        "field_name": "created_at",
        "filter_type": "sqlalchemy.and_",
        "op": ">=",
        "value": datetime.date(2022, 5, 10),
    }

# testes