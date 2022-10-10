from unittest.mock import MagicMock, patch

from alfred.response import Response, ResponseError


@patch("alfred.response.Response._query_response")
def test_response_new_with_query_without_pages(mock_query_response):
    query = MagicMock()
    Response(200, headers={"header": "value"}, query=query)

    mock_query_response.assert_called_once_with(
        status_code=200,
        headers={"header": "value"},
        query=query,
        per_page=20,
        page=1,
        model_property="to_json",
    )


@patch("alfred.response.Response._query_response")
def test_response_new_with_query_with_pages(mock_query_response):
    query = MagicMock()
    Response(200, headers={"header": "value"}, query=query, per_page=50, page=2)

    mock_query_response.assert_called_once_with(
        status_code=200,
        headers={"header": "value"},
        query=query,
        per_page=50,
        page=2,
        model_property="to_json",
    )


@patch("alfred.response.Response._simple_response")
def test_response_new_with_body(mock_simple_response):
    body = MagicMock()
    Response(200, headers={"header": "value"}, body=body)

    mock_simple_response.assert_called_once_with(
        status_code=200, headers={"header": "value"}, body=body
    )


@patch("alfred.response.response.ChaliceResponse")
def test_query_response_whith_default_pagination(mock_chalice_response):
    query = MagicMock()
    obj1 = MagicMock(to_json={"obj": "1"})
    obj2 = MagicMock(to_json={"obj": "2"})
    query.all.return_value = [obj1, obj2]
    query.count.return_value = len(query.all.return_value)

    response = Response(200, headers={"header": "value"}, query=query)
    assert response is not None


@patch("alfred.response.response.ChaliceResponse")
def test_query_response_whith_custom_pagination(mock_chalice_response):
    query = MagicMock()
    obj1 = MagicMock(to_json={"obj": "1"})
    obj2 = MagicMock(to_json={"obj": "2"})
    obj3 = MagicMock(to_json={"obj": "3"})
    obj4 = MagicMock(to_json={"obj": "4"})
    obj5 = MagicMock(to_json={"obj": "5"})
    query.all.return_value = [obj1, obj2, obj3, obj4, obj5]
    query.count.return_value = len(query.all.return_value)

    response = Response(
        200, headers={"header": "value"}, query=query, per_page=2, page=5
    )
    assert response is not None


def test_return_query_response_with_next_page():
    query = MagicMock()
    obj1 = MagicMock(to_json={"obj": "1"})
    obj2 = MagicMock(to_json={"obj": "2"})
    obj3 = MagicMock(to_json={"obj": "3"})
    obj4 = MagicMock(to_json={"obj": "4"})
    obj5 = MagicMock(to_json={"obj": "5"})
    query.all.return_value = [obj1, obj2, obj3, obj4, obj5]
    query.count.return_value = len(query.all.return_value)

    response = Response(
        200, headers={"header": "value"}, query=query, per_page=2, page=3
    )

    assert response.body["next_page"] is not None


def test_return_query_response_without_next_page():
    query = MagicMock()
    obj1 = MagicMock(to_json={"obj": "1"})
    obj2 = MagicMock(to_json={"obj": "2"})
    obj3 = MagicMock(to_json={"obj": "3"})
    obj4 = MagicMock(to_json={"obj": "4"})
    obj5 = MagicMock(to_json={"obj": "5"})
    query.all.return_value = [obj1, obj2, obj3, obj4, obj5]
    query.count.return_value = len(query.all.return_value)

    response = Response(
        200, headers={"header": "value"}, query=query, per_page=2, page=5
    )

    assert response.body["next_page"] is None


@patch("alfred.response.response.ChaliceResponse")
def test_simple_response(mock_chalice_response):
    response = Response(200, headers={"header": "value"}, body={"foo": "bar"})

    mock_chalice_response.assert_called_once_with(
        status_code=200,
        body={"foo": "bar"},
        headers={"header": "value"},
    )

    assert response == mock_chalice_response.return_value


def test_parent_class():
    assert issubclass(ResponseError, Exception) is True


def test_response_error_init():
    err = ResponseError(200, "message")
    assert err.status_code == 200
    assert err.body == {"error": ["message"]}
    assert err.send_to_sentry is False


def test_response_error_init_with_send_to_sentry():
    err = ResponseError(200, "message", send_to_sentry=True)
    assert err.status_code == 200
    assert err.body == {"error": ["message"]}
    assert err.send_to_sentry is True


def test_response_error_init_with_extra():
    err = ResponseError(200, "message", extra={"foo": "bar"})
    assert err.status_code == 200
    assert err.body == {"error": ["message"], "_error_extra": {"foo": "bar"}}
    assert err.send_to_sentry is False


def test_response_error_init_with_error_in_extra():
    err = ResponseError(200, "message", extra={"error": "error message"})
    assert err.status_code == 200
    assert err.body == {
        "error": ["message"],
        "_error_extra": {"error": "error message"},
    }
    assert err.send_to_sentry is False
