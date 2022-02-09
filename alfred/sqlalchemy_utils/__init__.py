from alfred.aws.exceptions import S3UploadFileException
from alfred.aws.s3 import S3File
from alfred.storages import DummyStorage, DummyStorageException

STORAGE_SETTINGS = {
    "s3": {"class": S3File, "error": S3UploadFileException},
    "dummy": {"class": DummyStorage, "error": DummyStorageException},
}
