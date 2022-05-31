from functools import wraps
from hashlib import md5

from alfred.cache.walrus_cache import Cache


def cache_memoize(cache_time=60 * 60, is_classmethod=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            clean_args = args[1:] if is_classmethod else args
            cache_key = f"{func.__module__}.{func.__qualname__}:{clean_args}_{kwargs}"
            hash_key = md5(cache_key.encode()).hexdigest()

            cache = Cache()
            cached = cache.get(hash_key)
            if cached:
                return cached

            result = func(*args, **kwargs)
            cache.set(hash_key, result, cache_time)
            return result

        wrapper._decorator_name = "cache_memoize"
        return wrapper

    return decorator
