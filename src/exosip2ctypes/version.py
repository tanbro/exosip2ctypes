from ctypes import string_at

from ._c import conf
from .utils import b2s

__all__ = ['get_library_version']


def get_library_version():
    """
    :return: eXosip library version string
    :rtype: str
    """
    return b2s(string_at(conf.FuncGetVersion.c_func()))
