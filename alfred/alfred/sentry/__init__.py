import os

import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")


sentry_sdk.init(
    dsn=SENTRY_DSN, integrations=[AwsLambdaIntegration()],
)
