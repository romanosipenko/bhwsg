from django.shortcuts import _get_queryset
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
        

def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
