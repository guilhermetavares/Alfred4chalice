import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields.br_document import BRDocumentField


def test_brdocument_is_subclass():
    assert issubclass(BRDocumentField, fields.String)


def test_brdocument_invalid_default_message():
    field = BRDocumentField()
    document = "12309845687"

    with pytest.raises(ValidationError) as err:
        field._deserialize(document, "document", {"document": document})

    assert err.value.args[0] == "CPF inválido"


def test_brdocument_invalid_custom_message():
    document_err_msg = "Some error message"
    field = BRDocumentField(document_error_msg=document_err_msg)
    document = "12309845687"

    with pytest.raises(ValidationError) as err:
        field._deserialize(document, "document", {"document": document})

    assert err.value.args[0] == document_err_msg


def test_brdocument_valid_without_mask():
    field = BRDocumentField()
    document = "99241995025"

    value = field._deserialize(document, "document", {"document": document})

    assert value == "99241995025"


def test_brdocument_valid_with_mask():
    field = BRDocumentField()
    document = "615.179.300-57"

    value = field._deserialize(document, "document", {"document": document})

    assert value == "61517930057"
