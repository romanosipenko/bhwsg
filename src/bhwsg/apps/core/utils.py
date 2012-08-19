try:
    import simplejson as json
except ImportError:
    import json


def memoize_method(func):
    '''
        Call the object method just once for a args set and memoize the result
    '''
    key = func.__name__

    def inner(self, *args, **kwargs):
        try:
            cache = self._mm
        except AttributeError:
            cache = {}
            self._mm = cache

        key_args = key + (str(args) if args else '') + (str(kwargs) if kwargs else '')
        try:
            res = cache[key_args]
        except KeyError:
            res = func(self, *args, **kwargs)
            cache[key_args] = res

        return res
    return inner


def generate_username(email):
    username = email.split('@')[0]
    yield username
    i = 0
    while True:
        i += 1
        yield "%s%d" % (username, i)
