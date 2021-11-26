import os
from alfred.sentry import sentry_sdk
from walrus import Walrus


ALFRED_REDIS_HOST = os.environ.get("ALFRED_REDIS_HOST", "")


class WallrusException(Exception):
    pass


class Cache:
    @classmethod
    def _capture_sentry(self):
        err = WallrusException()
        sentry_sdk.capture_exception(err)

    @classmethod
    def _cache(self):
        return Walrus(host=ALFRED_REDIS_HOST, port=6379, db=0).cache()

    @classmethod
    def set(self, cache_key, value, expires_in):
        try:
            self._cache().set(cache_key, value, expires_in)
        except Exception:  # noqa
            self._capture_sentry()

    @classmethod
    def get(self, cache_key, default=None):
        try:
            return self._cache().get(cache_key, default)
        except Exception:  # noqa
            self._capture_sentry()
            return default
    
    @classmethod
    def delete(self, cache_key):
        try:
            return self._cache().delete(cache_key)
        except Exception:  # noqa
            self._capture_sentry()
