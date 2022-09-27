import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields.br_company_registry import BRCompanyRegistryField


def test_br_company_registry_is_subclass():
    assert issubclass(BRCompanyRegistryField, fields.String)


def test_br_company_registry_invalid_default_message():
    field = BRCompanyRegistryField()
    document = "12309845687010"

    with pytest.raises(ValidationError) as err:
        field._deserialize(document, "document", {"document": document})

    assert err.value.args[0] == "CNPJ inválido"


def test_br_company_registry_invalid_custom_message():
    document_err_msg = "Some error message"
    field = BRCompanyRegistryField(document_error_msg=document_err_msg)
    document = "12309845687010"

    with pytest.raises(ValidationError) as err:
        field._deserialize(document, "document", {"document": document})

    assert err.value.args[0] == document_err_msg


def test_br_company_registry_valid_without_mask():
    field = BRCompanyRegistryField()
    document = "03492539000101"

    value = field._deserialize(document, "document", {"document": document})

    assert value == "03492539000101"


def test_company_document_valid_with_mask():
    field = BRCompanyRegistryField()
    document = "03.492.539/0001-01"

    value = field._deserialize(document, "document", {"document": document})

    assert value == "03492539000101"
