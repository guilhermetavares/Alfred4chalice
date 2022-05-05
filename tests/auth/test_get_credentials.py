import base64

import pytest

from alfred.auth.utils import get_credentials


def test_get_credentials_success():
    auth64 = base64.b64encode(b"foo:bar")
    username, password = get_credentials(auth64)

    assert username == "foo"
    assert password == "bar"


@pytest.mark.parametrize(
    "auth64",
    ["ibnnacoiamçlsmocc", base64.b64encode(b"foo")],
)
def test_get_credentials_error(auth64):
    username, password = get_credentials(auth64)

    assert username is None
    assert password is None
