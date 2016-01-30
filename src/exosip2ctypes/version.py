from ctypes import string_at

from ._c import conf

__all__ = ['get_library_version']


def get_library_version():
    return string_at(conf.FuncGetVersion.c_func()).decode()

