from marshmallow import ValidationError, fields

from validate_docbr import CPF
from alfred.tools import only_digits

class BRDocumentField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        cpf = only_digits(value)
        valid_CPF = CPF().validate(value)

        if not valid_CPF:
            raise ValidationError(self.error_messages["document_error_msg"])

        return cpf

    def __init__(self, document_error_msg="CPF inválido"):
        super().__init__()
        self.error_messages["document_error_msg"] = document_error_msg

