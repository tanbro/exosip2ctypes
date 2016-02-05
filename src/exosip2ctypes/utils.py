# -*- coding: utf-8 -*-

"""
some helper functions
"""

from .error import OsipError, OSIP_SUCCESS

__all__ = ['b2s', 's2b', 'raise_if_osip_error']


def b2s(s):
    if bytes != str:
        if isinstance(s, bytes):
            return s.decode()
    return s


def s2b(s):
    if bytes != str:
        if isinstance(s, str):
            return s.encode()
    return s


def raise_if_osip_error(err_code):
    """raise an :exception:`OsipError` exception if `err_code` is not :var:`OSIP_SUCCESS`

    use it to check osip2/eXosip2 API function integer return value
    :param int err_code:
    :raises OsipError: if `err_code` is not zero
    """
    if int(err_code) != OSIP_SUCCESS:
        raise OsipError(err_code)
