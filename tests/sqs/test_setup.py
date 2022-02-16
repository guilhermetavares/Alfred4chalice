import json
from unittest.mock import patch

import pytest
from chalice.app import SQSEvent

from alfred.sqs.exceptions import SQSTaskError
from alfred.sqs.setup import handle_sqs_message
from alfred.sqs.sqs import SQSTask


@SQSTask()
def foo(param_a, param_b):
    return {"param_a": param_a, "param_b": param_b}


@patch("alfred.sqs.setup.logger")
def test_handle_sqs_message_successful(mock_logger, sqs_stub):
    sqs_stub.add_response("delete_message", service_response={})
    body = json.dumps(
        {
            "_func_module": "tests.sqs.test_setup",
            "_func_name": "foo",
            "args": [123],
            "kwargs": {"param_b": "bar"},
            "retries": 0,
        }
    )
    record = {"body": body, "receiptHandle": "foo-receipt-handle"}
    event_dict = {"Records": [record]}

    event = SQSEvent(event_dict=event_dict, context="")

    handle_sqs_message(event)

    mock_logger.debug.assert_called_once_with(
        {
            "task_has_succeeded": True,
            "task_error_message": None,
            "task_function_module": "tests.sqs.test_setup",
            "task_function_name": "foo",
            "task_function_args": [123],
            "task_function_kwargs": {"param_b": "bar"},
            "task_function_retries": 0,
            "task_response": {"param_a": 123, "param_b": "bar"},
        }
    )


@SQSTask()
def foo_error(param_a, param_b):
    raise SQSTaskError("Error message")


@patch("alfred.sqs.setup.logger")
def test_handle_sqs_message_unsuccessful(mock_logger, sqs_stub):
    sqs_stub.add_response("delete_message", service_response={})
    body = json.dumps(
        {
            "_func_module": "tests.sqs.test_setup",
            "_func_name": "foo_error",
            "args": [123],
            "kwargs": {"param_b": "bar"},
            "retries": 0,
        }
    )
    record = {"body": body, "receiptHandle": "foo-receipt-handle"}
    event_dict = {"Records": [record]}

    event = SQSEvent(event_dict=event_dict, context="")

    with pytest.raises(SQSTaskError):
        handle_sqs_message(event)

    mock_logger.debug.assert_called_once_with(
        {
            "task_has_succeeded": False,
            "task_error_message": "Error message",
            "task_function_module": "tests.sqs.test_setup",
            "task_function_name": "foo_error",
            "task_function_args": [123],
            "task_function_kwargs": {"param_b": "bar"},
            "task_function_retries": 0,
            "task_response": None,
        }
    )
