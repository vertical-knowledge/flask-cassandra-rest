__author__ = 'Tim Martin'
from cassandra.util import sortedset
from datetime import datetime, timedelta
from decimal import Decimal
import inspect
import re


class ClassPropertyDescriptor(object):
    """
    Straight up stolen from stack overflow
    Implements class level properties
    http://stackoverflow.com/questions/5189699/how-can-i-make-a-class-property-in-python
    """

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    """
    Using this decorator a class can have a decorator. Necessary for dynamically settings urls
    on application/blueprint

    :param func: The function to wrap
    :type func: function
    :rtype: ClassPropertyDescriptor
    """
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


def get_class_that_defined_method(meth):
    for cls in inspect.getmro(meth.im_class):
        if meth.__name__ in cls.__dict__:
            return cls
    return None


_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def convert_to_underscore(toconvert):
    """
    Converts a string from CamelCase to underscore

    :param toconvert: The string to convert from CamelCase to underscore (i.e. camel_case)
    :type toconvert: str
    :return: The converted string
    :rtype: str
    """
    i = 0
    while toconvert[i] == '_':
        i += 1
    prefix = None
    if i > 0:
        prefix = toconvert[0:i]
        toconvert = toconvert[i:]
    s1 = _first_cap_re.sub(r'\1_\2', toconvert)
    s2 = _all_cap_re.sub(r'\1_\2', s1).lower()
    if prefix is not None:
        return '{0}{1}'.format(prefix, s2)
    return s2


def make_json_serializable(value):
    if isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S.%f')
    elif isinstance(value, set) or isinstance(value, sortedset):
        return list(value)
    else:
        return value


def convert_to_datetime(d):
    """
    For webargs so that it can correctly parse incoming datetime objects

    :param d: A datetime string formatted as %Y-%m-%d %H:%M:%S.%f
    :type d: str
    :return: The datetime object
    :rtype: datetime
    """
    if type(d) == datetime:
        return d
    d = datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')
    # remove the resolution that cassandra can't handle
    td = timedelta(microseconds=d.microsecond % 1000)
    return d - td


def convert_to_boolean(val):
    """
    Converts a string of either "True" or "False" case-insensitive into a boolean

    :param val: The true or false string
    :type val: str
    :return: The mapped boolean
    :rtype: bool
    """
    if type(val) == bool:
        return val
    elif val is None:
        return val
    elif val.lower() == 'false':
        return False
    elif val.lower() == 'true':
        return True
    else:
        raise ValueError('A boolean value accepted as a string must be either "true" or "false"')