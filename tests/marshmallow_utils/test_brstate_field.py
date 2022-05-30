import pytest
from marshmallow import ValidationError, fields

from alfred.marshmallow_utils.fields.br_state import BRStateField


def test_brstate_is_subclass():
    assert issubclass(BRStateField, fields.String)


def test_brstate_invalid_state_default_message():
    field = BRStateField()
    state = "sp"

    with pytest.raises(ValidationError) as err:
        field._deserialize(state, "state", {"state": state})

    assert err.value.args[0] == "Estado inválido"


def test_brstate_invalid_state_custom_message():
    state_error_msg = "Some error message"
    field = BRStateField(state_error_msg=state_error_msg)
    state = "sp"

    with pytest.raises(ValidationError) as err:
        field._deserialize(state, "state", {"state": state})

    assert err.value.args[0] == state_error_msg


def test_brstate_valid():
    field = BRStateField()
    state = "SP"

    value = field._deserialize(state, "state", {"state": state})

    assert value == state
