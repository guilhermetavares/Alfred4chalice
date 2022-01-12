from alfred.cache.walrus_cache import Cache
from functools import wraps


def cache_memoize(cache_key, cache_time):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = Cache()
            cached = cache.get(cache_key)
            if cached:
                return cached

            result = func(*args, **kwargs)
            cache.set()
            return f"{cache_key} - {cache_time}"

        wrapper._decorator_name = "cache_memoize"
        return wrapper

    return decorator

@cache_memoize(cache_key="somar", cache_time=100)
def somar(num1, num2):
    return num1+num2
