import json
import uuid
from unittest.mock import patch
from botocore.exceptions import ClientError

import pytest

from alfred.settings import SQS_QUEUE_URL
from alfred.sqs.exceptions import SQSTaskError, SQSTaskMaxRetriesExceededError
from alfred.sqs.sqs import SQSHandler, SQSTask
from tests.tools import sqs_expected_params


def test_sqs_task_error():
    assert issubclass(SQSTaskError, Exception) is True


def test_sqs_task_max_retries_exceeded_error():
    assert issubclass(SQSTaskMaxRetriesExceededError, Exception) is True


def test_sqs_task_queue_url_property():
    assert SQSTask.default_queue_url == SQS_QUEUE_URL


def test_sqs_task_default_delay_property():
    assert SQSTask.default_delay == 1


def test_sqs_task_max_retries_property():
    assert SQSTask.max_retries == 3


def test_sqs_task_default_retry_delay_property():
    assert SQSTask.default_retry_delay == 60 * 3


@SQSTask()
def foo(param_a, param_b):
    return "bar"


def test_sqs_task_init():
    assert foo.bind is False
    assert foo.retries == 0


def test_sqs_task_apply():
    response = foo.apply(args=["fubar"], kwargs={"param_b": 10})
    assert response == "bar"


@patch("alfred.sqs.sqs.sentry_sdk")
@patch("alfred.sqs.sqs.sqs_client")
def test_apply_side_effect_async(mock_sqs_client, mock_sentry):
    response = foo.apply_async(args=["fubar"], kwargs={"param_b": 10})
    mock_sqs_client.send_message.side_effect = ClientError
    mock_sentry.assert_called_onde()


@patch("alfred.sqs.sqs.sqs_client")
def test_apply_async(mock_sqs_client):
    response = foo.apply_async(args=["fubar"], kwargs={"param_b": 10})

    mock_sqs_client.send_message.assert_called_once_with(
        QueueUrl=foo.queue_url,
        DelaySeconds=foo.default_delay,
        MessageBody=json.dumps(
            {
                "_func_module": foo.func.__module__,
                "_func_name": foo.func.__name__,
                "args": ["fubar"],
                "kwargs": {"param_b": 10},
                "retries": 0,
            }
        ),
    )
    assert response == mock_sqs_client.send_message.return_value["MessageId"]


@patch("alfred.sqs.sqs.sqs_client")
def test_apply_async_with_countdown(mock_sqs_client):
    response = foo.apply_async(args=["fubar"], kwargs={"param_b": 10}, countdown=30,)

    mock_sqs_client.send_message.assert_called_once_with(
        QueueUrl=foo.queue_url,
        DelaySeconds=30,
        MessageBody=json.dumps(
            {
                "_func_module": foo.func.__module__,
                "_func_name": foo.func.__name__,
                "args": ["fubar"],
                "kwargs": {"param_b": 10},
                "retries": 0,
            }
        ),
    )
    assert response == mock_sqs_client.send_message.return_value["MessageId"]


@patch("alfred.sqs.sqs.sqs_client")
def test_apply_async_with_queue_url(mock_sqs_client):
    response = foo.apply_async(
        args=["fubar"], kwargs={"param_b": 10}, queue_url="fake-queue",
    )

    mock_sqs_client.send_message.assert_called_once_with(
        QueueUrl="fake-queue",
        DelaySeconds=foo.default_delay,
        MessageBody=json.dumps(
            {
                "_func_module": foo.func.__module__,
                "_func_name": foo.func.__name__,
                "args": ["fubar"],
                "kwargs": {"param_b": 10},
                "retries": 0,
            }
        ),
    )
    assert response == mock_sqs_client.send_message.return_value["MessageId"]


def test_sqs_handler_init():
    body = {"foo": "bar"}
    handler = SQSHandler(json.dumps(body))

    assert handler.body == body


def test_sqs_handler_apply():
    body = {
        "_func_module": foo.func.__module__,
        "_func_name": foo.func.__name__,
        "args": ["fubar"],
        "kwargs": {"param_b": 10},
        "retries": 1,
    }
    handler = SQSHandler(json.dumps(body))
    response = handler.apply()

    assert response == "bar"


@patch("alfred.sqs.sqs.sqs_client")
def test_sqs_handler_sqs_delete_message(mock_sqs_client):
    body = {"foo": "bar"}
    handler = SQSHandler(json.dumps(body))
    handler.sqs_delete_message("fake-queue", "fake-receipt-handle")

    mock_sqs_client.delete_message.assert_called_once_with(
        QueueUrl="fake-queue", ReceiptHandle="fake-receipt-handle"
    )


@SQSTask(bind=True)
def foo_with_retry(self, param_a, param_b):
    try:
        resp = 10 + "bar"
    except TypeError as err:
        return self.retry(err=err, max_retries=3, countdown=500)
    return resp


@patch("alfred.sqs.sqs.sentry_sdk")
def test_sqs_task_retry(sentry_sdk, sqs_stub):
    expected_params_send_sms = sqs_expected_params(
        foo_with_retry,
        task_args=["fubar"],
        task_kwargs={"param_b": 10},
        task_countdown=500,
        task_retries=1,
    )
    sqs_stub.add_response(
        "send_message",
        service_response={"MessageId": str(uuid.uuid4())},
        expected_params=expected_params_send_sms,
    )

    body = {
        "_func_module": foo_with_retry.func.__module__,
        "_func_name": foo_with_retry.func.__name__,
        "args": ["fubar"],
        "kwargs": {"param_b": 10},
        "retries": 0,
    }
    handler = SQSHandler(json.dumps(body))
    response = handler.apply()

    assert response is None
    sentry_sdk.capture_message.assert_called_once_with(
        "unsupported operand type(s) for +: 'int' and 'str'"
    )


@patch("alfred.sqs.sqs.sentry_sdk")
def test_sqs_task_retry_raise_max_retries_exceeded(sentry_sdk, sqs_stub):
    body = {
        "_func_module": foo_with_retry.func.__module__,
        "_func_name": foo_with_retry.func.__name__,
        "args": ["fubar"],
        "kwargs": {"param_b": 10},
        "retries": 2,
    }
    handler = SQSHandler(json.dumps(body))
    with pytest.raises(SQSTaskMaxRetriesExceededError):
        handler.apply()

    sentry_sdk.assert_not_called()
