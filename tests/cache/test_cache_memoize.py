from alfred.cache.cache_decorator import cache_memoize
from unittest.mock import patch


@cache_memoize(cache_time=1)
def somar(num1, num2, **kwargs):
    return num1+num2


@patch("alfred.cache.cache_decorator.Cache.set")
@patch("alfred.cache.cache_decorator.Cache.get")
def test_cache_memoize_decorator_with_cache(mock_cache_get, mock_cache_set):
    mock_cache_get.return_value = "7cc994ae11c81bb4844d4e6d86de253c"
    somar(1, 1)

    mock_cache_get.assert_called_once_with(mock_cache_get.return_value)
    mock_cache_set.assert_not_called()


@patch("alfred.cache.cache_decorator.Cache.set")
@patch("alfred.cache.cache_decorator.Cache.get")
def test_cache_memoize_decorator_without_cache(mock_cache_get, mock_cache_set):
    mock_cache_get.return_value = None
    somar(1, 1)

    mock_cache_set.assert_called_once_with('7cc994ae11c81bb4844d4e6d86de253c', 2, 1)
