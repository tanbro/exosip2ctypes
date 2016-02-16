from ctypes import string_at

from ._c import conf
from .utils import to_str

__all__ = ['version', 'get_library_version']

#: version of the package
version = '0.1'


def get_library_version():
    """
    :return: eXosip library (C library) version string
    :rtype: str
    """
    return to_str(string_at(conf.FuncGetVersion.c_func()))
