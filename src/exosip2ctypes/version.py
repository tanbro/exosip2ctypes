# -*- coding: utf-8 -*-

"""
version infomation
"""

from __future__ import absolute_import, unicode_literals
from pkg_resources import get_distribution

__all__ = ['__version__', 'get_library_version']


# pylint: disable=C0103
__version__ = get_distribution('exosip2ctypes').version  # type: str


def get_library_version():
    """
    :return: eXosip library (C library) version string
    :rtype: str
    """

    from ._c import conf
    from .utils import to_str

    return to_str(conf.FuncGetVersion.c_func())
