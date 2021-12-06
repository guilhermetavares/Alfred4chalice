import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

from alfred.settings import SENTRY_DSN

sentry_sdk.init(
    dsn=SENTRY_DSN, integrations=[AwsLambdaIntegration()],
)
