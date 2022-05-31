from hashlib import md5
from unittest.mock import patch

from alfred.cache.cache_decorator import cache_memoize


@cache_memoize(cache_time=1)
def somar(num1, num2, **kwargs):
    return num1 + num2


@patch("alfred.cache.cache_decorator.Cache.set")
@patch("alfred.cache.cache_decorator.Cache.get")
def test_cache_memoize_decorator_with_cache(mock_cache_get, mock_cache_set):
    mock_cache_get.return_value = 2

    cache_key = "tests.cache.test_cache_memoize.somar:(1, 1)_{}"
    hash_key = md5(cache_key.encode()).hexdigest()

    assert somar(1, 1) == 2

    mock_cache_get.assert_called_once_with(hash_key)
    mock_cache_set.assert_not_called()


@patch("alfred.cache.cache_decorator.Cache.set")
@patch("alfred.cache.cache_decorator.Cache.get")
def test_cache_memoize_decorator_without_cache(mock_cache_get, mock_cache_set):
    mock_cache_get.return_value = None

    cache_key = "tests.cache.test_cache_memoize.somar:(1, 1)_{}"
    hash_key = md5(cache_key.encode()).hexdigest()

    assert somar(1, 1) == 2

    mock_cache_get.assert_called_once_with(hash_key)
    mock_cache_set.assert_called_once_with(hash_key, 2, 1)


class TestClass:
    @cache_memoize(cache_time=1, is_classmethod=True)
    def somar(self, num1, num2, **kwargs):
        return num1 + num2


@patch("alfred.cache.cache_decorator.Cache.set")
@patch("alfred.cache.cache_decorator.Cache.get")
def test_cache_memoize_decorator_with_cache_and_is_classmethod_true(
    mock_cache_get, mock_cache_set
):
    mock_cache_get.return_value = 2

    cache_key = "tests.cache.test_cache_memoize.TestClass.somar:(1, 1)_{}"
    hash_key = md5(cache_key.encode()).hexdigest()

    assert TestClass().somar(1, 1) == 2

    mock_cache_get.assert_called_once_with(hash_key)
    mock_cache_set.assert_not_called()


@patch("alfred.cache.cache_decorator.Cache.set")
@patch("alfred.cache.cache_decorator.Cache.get")
def test_cache_memoize_decorator_without_cache_and_is_classmethod_true(
    mock_cache_get, mock_cache_set
):
    mock_cache_get.return_value = None

    cache_key = "tests.cache.test_cache_memoize.TestClass.somar:(1, 1)_{}"
    hash_key = md5(cache_key.encode()).hexdigest()

    assert TestClass().somar(1, 1) == 2

    mock_cache_get.assert_called_once_with(hash_key)
    mock_cache_set.assert_called_once_with(hash_key, 2, 1)
