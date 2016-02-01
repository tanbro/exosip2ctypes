# -*- coding: utf-8 -*-

"""
some helper functions
"""

from .error import ApiReturnError

__all__ = ['raise_if_not_zero']


def raise_if_not_zero(err_code):
    """raise an :exception:`ApiReturnError` exception if `err_code` is not zero

    use it to check eXosip2 API function integer return value
    :param int err_code:
    :raises ApiReturnError: if `err_code` is not zero
    """
    err_code = int(err_code)
    if err_code != 0:
        raise ApiReturnError(err_code)
