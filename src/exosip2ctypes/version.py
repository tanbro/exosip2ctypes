from ._c import conf
from .utils import to_str

__all__ = ['get_library_version']


def get_library_version():
    """
    :return: eXosip library (C library) version string
    :rtype: str
    """
    return to_str(conf.FuncGetVersion.c_func())
