from sqlalchemy import types

from alfred.settings import DEFAULT_STORAGE
from alfred.sqlalchemy_utils import STORAGE_SETTINGS


class ImageType(types.TypeDecorator):
    impl = types.Unicode(128)

    def __init__(self, upload_to):
        super(ImageType, self).__init__()

        self.upload_to = upload_to

        self.storage_config = STORAGE_SETTINGS[DEFAULT_STORAGE]
        self.storage_error = self.storage_config["error"]
        self.storage_class = self.storage_config["class"]
        self.storage = self.storage_class()

    def process_bind_param(self, value, dialect):
        success, file_name = self.storage.upload_file(value, upload_to=self.upload_to)

        if not success:
            raise self.storage_error("Upload do arquivo não pode ser realizado")

        return file_name

    def process_result_value(self, value, dialect):
        url = self.storage.get_presigned_url(value)

        return url
