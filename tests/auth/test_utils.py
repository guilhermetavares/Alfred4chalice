from alfred.auth.utils import _fernet_fields


def test_fernet_fields_empty_kwargs():
    payload = {}
    encrypted_fields = ["any"]
    method = "encrypt"

    resp = _fernet_fields(encrypted_fields, method, **payload)

    assert resp == payload


def test_fernet_fields_wrong_method():
    payload = {"foo": "bar"}
    encrypted_fields = ["any"]
    method = "wrong_method"

    resp = _fernet_fields(encrypted_fields, method, **payload)

    assert resp == payload


def test_fernet_fields_empty_encrypted_fields():
    payload = {"foo": "bar"}
    encrypted_fields = []
    method = "wrong_method"

    resp = _fernet_fields(encrypted_fields, method, **payload)

    assert resp == payload
