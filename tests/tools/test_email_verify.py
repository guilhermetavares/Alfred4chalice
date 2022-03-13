from unittest.mock import patch

import pytest
from requests import ConnectTimeout, ReadTimeout, Timeout

from alfred.tools.email_verify import EmailListVerifyOne


@pytest.mark.vcr
def test_email_valid_success():
    email = "contato@maistodos.com.br"
    client = EmailListVerifyOne()
    assert client.verify(email) is True


@pytest.mark.vcr
def test_email_invalid_success():
    email = "invalid.email@maistodos.com.br"
    client = EmailListVerifyOne()
    assert client.verify(email) is False


@pytest.mark.parametrize(
    "err", (Timeout, ConnectTimeout, ReadTimeout, KeyError, TypeError)
)
@patch("alfred.tools.email_verify.requests.get")
def test_email_valid_error(mock_get, err):
    mock_get.side_effect = err
    email = "valid.email@maistodos.com.br"
    client = EmailListVerifyOne()
    assert client.verify(email) is True
