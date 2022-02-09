from unittest.mock import patch

import pytest
from sqlalchemy import types

from alfred.aws.exceptions import S3UploadFileException
from alfred.sqlalchemy_utils.fields import ImageType


def test_image_type_as_type_decorator():
    assert issubclass(ImageType, types.TypeDecorator) is True


def test_image_type_impl():
    assert type(ImageType.impl) is types.Unicode
    assert ImageType.impl.length == 128


@patch("alfred.sqlalchemy_utils.fields.image.DEFAULT_STORAGE", "s3")
def test_image_type_s3_process_bind_param_sucess(s3_stub):
    s3_stub.add_response(
        "put_object", service_response={},
    )

    file_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwC"
    "AAAAC0lEQVR42mNkWAsAALMAr6o4KHcAAAAASUVORK5CYII="

    t = ImageType(upload_to="avatars")
    file_name = t.process_bind_param(value=file_base64, dialect="object")

    assert file_name is not None


@patch("alfred.sqlalchemy_utils.fields.image.DEFAULT_STORAGE", "s3")
def test_image_type_s3_process_bind_param_exception():
    file_base64 = "some_fake_base_64"

    t = ImageType(upload_to="avatars")

    with pytest.raises(S3UploadFileException):
        t.process_bind_param(value=file_base64, dialect="object")


@patch("alfred.sqlalchemy_utils.fields.image.DEFAULT_STORAGE", "s3")
def test_image_type_s3_process_result_value_sucess():
    file_name = "avatars/110fdf29-650f-480b-a01d-29b8f4788cb6.png"

    t = ImageType(upload_to="avatars")
    url = t.process_result_value(value=file_name, dialect="object")

    assert url is not None


@patch("alfred.sqlalchemy_utils.fields.image.DEFAULT_STORAGE", "dummy")
def test_image_type_dummy_process_bind_param_sucess(s3_stub):

    file_base64 = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwC"
    "AAAAC0lEQVR42mNkWAsAALMAr6o4KHcAAAAASUVORK5CYII="

    t = ImageType(upload_to="avatars")
    file_name = t.process_bind_param(value=file_base64, dialect="object")

    assert file_name == "dummy.file"


@patch("alfred.sqlalchemy_utils.fields.image.DEFAULT_STORAGE", "dummy")
def test_image_type_dummy_process_result_value_sucess():
    file_name = "dummy.file"

    t = ImageType(upload_to="avatars")
    url = t.process_result_value(value=file_name, dialect="object")

    assert url == file_name
