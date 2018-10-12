"""
  Created by kebo on 2018/10/9
"""
from functools import wraps
from flask import current_app, request
# from werkzeug.contrib.cache import SimpleCache

# cache = SimpleCache()

# 给cache增加删除具有指定关键字的cache_key的缓存的方法
def delete_like(self, kw):
    cache_keys = self.cache._cache.keys()
    del_keys = []
    for key in cache_keys:
        if kw in key:
            del_keys.append(key)
    self.delete_many(*del_keys)


# 重写make_cache_key, 解决分页共用缓存问题
def cached(self, timeout=None, key_prefix='view/%s', unless=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            #: Bypass the cache entirely.
            if callable(unless) and unless() is True:
                return f(*args, **kwargs)

            try:
                cache_key = decorated_function.make_cache_key(*args, **kwargs)
                rv = self.cache.get(cache_key)
            except Exception:
                if current_app.debug:
                    raise
                return f(*args, **kwargs)

            if rv is None:
                rv = f(*args, **kwargs)
                try:
                    self.cache.set(cache_key, rv,
                                   timeout=decorated_function.cache_timeout)
                except Exception:
                    if current_app.debug:
                        raise
                    return f(*args, **kwargs)
            return rv

        def make_cache_key(*args, **kwargs):
            if callable(key_prefix):
                cache_key = key_prefix()
            elif '%s' in key_prefix:
                cache_key = key_prefix % request.full_path  # 将这里改为了request.url, 原来是 request.path
            else:
                cache_key = key_prefix

            return cache_key

        decorated_function.uncached = f
        decorated_function.cache_timeout = timeout
        decorated_function.make_cache_key = make_cache_key

        return decorated_function

    return decorator



# def cached(timeout=5 * 60, key='view_%s'):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             p = request.args.get('page', None)
#             cache_key = ('get_item_%s' % p) if p else key % request.path
#             print(cache_key)
#             value = cache.get(cache_key)
#             if value is None:
#                 value = f(*args, **kwargs)
#                 cache.set(cache_key, value, timeout=timeout)
#             return value
#         return decorated_function
#     return decorator