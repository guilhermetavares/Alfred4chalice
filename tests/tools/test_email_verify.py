import pytest
from unittest.mock import patch
from requests import Timeout, ReadTimeout, ConnectTimeout

from alfred.tools.email_verify import EmailListVerifyOne


@pytest.mark.vcr
def test_email_valid_success():
    key = "fake_key"
    email = "valid.email@maistodos.com.br"
    client = EmailListVerifyOne(key, email)
    assert client.verify() is True


@pytest.mark.vcr
def test_email_invalid_success():
    key = "fake_key"
    email = "invalid.email@maistodos.com.br"
    client = EmailListVerifyOne(key, email)
    assert client.verify() is False


@pytest.mark.parametrize("err", (Timeout, ConnectTimeout, ReadTimeout, KeyError, TypeError))
@patch("alfred.tools.email_verify.requests.get")
def test_email_valid_error(mock_get, err):
    mock_get.side_effect = err
    key = "fake_key"
    email = "valid.email@maistodos.com.br"
    client = EmailListVerifyOne(key, email)
    assert client.verify() is True
