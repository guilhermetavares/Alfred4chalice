from unittest.mock import patch

import pytest
from requests import ConnectTimeout, ReadTimeout, Timeout

from alfred.tools.email_verify import EmailListVerifyOne, is_smtp_email_valid


@pytest.mark.vcr
def test_email_control():
    email = "contato@maistodos.com.br"
    assert EmailListVerifyOne.control(email) == "ok"


@patch("alfred.tools.email_verify.EmailListVerifyOne.control")
def test_email_valid_success(mock_control):
    mock_control.return_value = "ok"
    email = "email@maistodos.com.br"
    assert EmailListVerifyOne.verify(email) is True


@patch("alfred.tools.email_verify.EmailListVerifyOne.control")
def test_email_invalid_success(mock_control):
    mock_control.return_value = "email_disabled"
    email = "email@maistodos.com.br"
    assert EmailListVerifyOne.verify(email) is False


@pytest.mark.parametrize(
    "err", (Timeout, ConnectTimeout, ReadTimeout, KeyError, TypeError)
)
@patch("alfred.tools.email_verify.requests.get")
def test_email_valid_error(mock_get, err):
    mock_get.side_effect = err
    email = "valid.email@maistodos.com.br"
    assert EmailListVerifyOne.verify(email) is True


@pytest.mark.vcr
def test_is_smtp_email_valid_skip_api():
    assert is_smtp_email_valid("wrong valid email") is False
    assert is_smtp_email_valid("valid.email@maistodos.com.br") is True


@pytest.mark.vcr
def test_is_smtp_email_valid_rate_api():
    email = "contato@maistodos.com.br"
    assert is_smtp_email_valid(email, force=True) is True
