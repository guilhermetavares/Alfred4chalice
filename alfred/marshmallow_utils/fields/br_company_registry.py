from marshmallow import ValidationError, fields
from pycpfcnpj import cnpj

from alfred.tools.core import only_digits


class BRCompanyRegistryField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        document = only_digits(value)
        valid_CNPJ = cnpj.validate(value)

        if not valid_CNPJ:
            raise ValidationError(self.error_messages["document_error_msg"])

        return document

    def __init__(self, document_error_msg="CNPJ inválido", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["document_error_msg"] = document_error_msg
