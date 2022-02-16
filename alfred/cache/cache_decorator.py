from alfred.cache.walrus_cache import Cache
from functools import wraps
from hashlib import md5


def cache_memoize(cache_time=60*60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            cache_key = f"{func.__module__}.{func.__name__}:{args}_{kwargs}"
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
