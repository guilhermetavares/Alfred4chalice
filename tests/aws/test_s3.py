import base64
from unittest.mock import patch

from botocore.exceptions import ClientError

from alfred.aws.s3 import S3File
from alfred.settings import BUCKET_S3

# this variable bellow represent a real image PNG semi transparent with
# color black. font: https://png-pixel.com/
image_base64 = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAA"
    "AAC0lEQVR42mNkWAsAALMAr6o4KHcAAAAASUVORK5CYII="
)


def test_extensions_dict():
    assert S3File.EXTENSIONS["image/png"] == "png"
    assert S3File.EXTENSIONS["image/jpg"] == "jpg"
    assert S3File.EXTENSIONS["image/jpeg"] == "jpg"


def test_random_file_name():
    data = "data:image/png;base64"
    ret = S3File._random_file_name(data)
    assert len(ret) == 40  # uuid (36) mais extensão, por exemplo .png (4)
    assert ret[-4:] == ".png"


@patch("alfred.aws.s3.S3File._random_file_name")
@patch("alfred.aws.s3.s3_client")
def test_upload_file(mock_s3_client, mock_random_file_name):
    response = S3File.upload_file(image_base64, upload_to="foo")

    body = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAA"
        "AAC0lEQVR42mNkWAsAALMAr6o4KHcAAAAASUVORK5CYII="
    )
    path = f"foo/{mock_random_file_name.return_value}"

    mock_random_file_name.assert_called_once_with("data:image/png;base64")
    mock_s3_client.put_object.assert_called_once_with(
        Body=body, Bucket=BUCKET_S3, Key=path
    )

    assert response == (True, path)


@patch("alfred.aws.s3.S3File._random_file_name")
@patch("alfred.aws.s3.s3_client")
def test_upload_file_with_file_name(mock_s3_client, mock_random_file_name):
    response = S3File.upload_file(image_base64, upload_to="foo", file_name="dummy.png")

    body = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAA"
        "AAC0lEQVR42mNkWAsAALMAr6o4KHcAAAAASUVORK5CYII="
    )
    path = "foo/dummy.png"

    mock_random_file_name.assert_not_called()
    mock_s3_client.put_object.assert_called_once_with(
        Body=body, Bucket=BUCKET_S3, Key=path
    )

    assert response == (True, path)


@patch("alfred.aws.s3.S3File._random_file_name")
@patch("alfred.aws.s3.s3_client")
def test_upload_file_s3_client_error(mock_s3_client, mock_random_file_name):
    mock_s3_client.put_object.side_effect = ClientError({"error": "some error"}, "")
    response = S3File.upload_file(image_base64, upload_to="foo")

    body = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAA"
        "AAC0lEQVR42mNkWAsAALMAr6o4KHcAAAAASUVORK5CYII="
    )
    path = f"foo/{mock_random_file_name.return_value}"

    mock_random_file_name.assert_called_once_with("data:image/png;base64")
    mock_s3_client.put_object.assert_called_once_with(
        Body=body, Bucket=BUCKET_S3, Key=path
    )

    assert response[0] is False
    assert "S3ClientError" in response[1]


@patch("alfred.aws.s3.S3File._random_file_name")
@patch("alfred.aws.s3.s3_client")
def test_upload_file_invalid_base64(mock_s3_client, mock_random_file_name):
    mock_s3_client.put_object.side_effect = ClientError({"error": "some error"}, "")
    response = S3File.upload_file("data:image/png;base64,a1b2c3", upload_to="foo")

    mock_random_file_name.assert_not_called()
    mock_s3_client.put_object.assert_not_called()

    assert response[0] is False
    assert "Base64Error" in response[1]


@patch("alfred.aws.s3.S3File._random_file_name")
@patch("alfred.aws.s3.s3_client")
def test_upload_file_not_base64_file(mock_s3_client, mock_random_file_name):
    mock_s3_client.put_object.side_effect = ClientError({"error": "some error"}, "")
    response = S3File.upload_file("base64_wrong", upload_to="foo")

    mock_random_file_name.assert_not_called()
    mock_s3_client.put_object.assert_not_called()

    assert response[0] is False
    assert "IndexError" in response[1]


@patch("alfred.aws.s3.s3_client")
def test_get_presigned_url(mock_s3_client):
    path = "foo/dummy.png"

    response = S3File.get_presigned_url(path)

    mock_s3_client.generate_presigned_url.assert_called_once_with(
        "get_object", Params={"Bucket": BUCKET_S3, "Key": path}
    )

    assert response == mock_s3_client.generate_presigned_url.return_value
