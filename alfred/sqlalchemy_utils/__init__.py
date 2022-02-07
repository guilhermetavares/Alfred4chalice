from alfred.aws import S3File, S3UploadFileException
from alfred.storages import DummyStorage, DummyStorageException

STORAGE_SETTINGS = {
    "s3": {"class": S3File, "error": S3UploadFileException},
    "dummy": {"class": DummyStorage, "error": DummyStorageException},
}
