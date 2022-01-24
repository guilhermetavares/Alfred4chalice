import os

# BASIC AUTH SETTINGS
ALFRED_PASSWORD_SALT = os.environ.get("ALFRED_PASSWORD_SALT")

# JWT_AUTH_SETTINGS
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXP_DELTA_SECONDS = int(os.environ.get("JWT_EXP_DELTA_SECONDS", "604800"))
JWT_SECRET = os.environ.get("JWT_SECRET")
FERNET_CRYPT_KEY = os.environ.get("FERNET_CRYPT_KEY")
JWT_CONTEXT_ARGS = ["device_id", "verify_code", "token"]

# CACHE SETTINGS
ALFRED_REDIS_HOST = os.environ.get("ALFRED_REDIS_HOST", "")

# SENTRY SETTINGS
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

# AWS SETTINGS
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "")
BUCKET_S3 = os.environ.get("BUCKET_S3", "")
DYNAMODB_HOST = os.environ.get("DYNAMODB_HOST")
DYNAMODB_PREFIX = os.environ.get("DYNAMODB_PREFIX")
