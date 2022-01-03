import json


def sqs_expected_params(
    task, task_args=[], task_kwargs={}, task_countdown=None, task_retries=None
):
    message_json = json.dumps(
        {
            "_func_module": task.func.__module__,
            "_func_name": task.func.__name__,
            "args": [*task_args],
            "kwargs": {**task_kwargs},
            "retries": task_retries or task.retries,
        }
    )

    return {
        "DelaySeconds": task_countdown or task.default_delay,
        "MessageBody": message_json,
        "QueueUrl": task.queue_url,
    }
