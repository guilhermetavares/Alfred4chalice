from unittest.mock import patch

from walrus.cache import Cache as LibCache
from alfred.cache.walrus_cache import Cache


def test_cache_init():
    cache = Cache._cache()
    assert isinstance(cache, LibCache)


def test_cache_get_by_default():
    default = "1"
    assert Cache.get("cache_key", default) == default


def test_cache_set_and_get():
    value = "1"
    Cache.set("cache_key", value, 60)
    assert Cache.get("cache_key") == value


def test_cache_delete():
    value = "1"
    Cache.set("cache_key", value, 60)
    assert Cache.get("cache_key") == value
    Cache.delete("cache_key")
    assert Cache.get("cache_key") is None


@patch("alfred.cache.walrus_cache.Cache._cache")
@patch("alfred.cache.walrus_cache.sentry_sdk.capture_exception")
def test_get_with_connection_error(capture_sentry, mock_cache):
    mock_cache.side_effect = Exception("erro conexao")
    default = "1"
    assert Cache.get("cache_key", default) == default
    capture_sentry.assert_called_once()


@patch("alfred.cache.walrus_cache.Cache._cache")
@patch("alfred.cache.walrus_cache.Cache._capture_sentry")
def test_set_with_connection_error(capture_sentry, mock_cache):
    mock_cache.side_effect = Exception("erro conexao")
    value = "1"
    Cache.set("cache_key", value, 60)
    capture_sentry.assert_called_once()


@patch("alfred.cache.walrus_cache.Cache._cache")
@patch("alfred.cache.walrus_cache.Cache._capture_sentry")
def test_delete_with_connection_error(capture_sentry, mock_cache):
    mock_cache.side_effect = Exception("erro conexao")
    Cache.delete("cache_key")
    capture_sentry.assert_called_once()
