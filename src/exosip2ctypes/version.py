# -*- coding: utf-8 -*-

"""
version infomation
"""

from __future__ import absolute_import, unicode_literals

__all__ = ['__version__', 'get_library_version']


__version__ = '1.2'


def get_library_version():
    """
    :return: eXosip library (C library) version string
    :rtype: str
    """

    from ._c import conf
    from .utils import to_str

    return to_str(conf.FuncGetVersion.c_func())
