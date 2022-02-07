class DummyStorage:
    def upload_file(cls, base64_file, upload_to, file_name="dummy.file", bucket=None):
        return True, file_name

    def get_presigned_url(cls, path, bucket=None):
        return path


class DummyStorageException(Exception):
    pass
