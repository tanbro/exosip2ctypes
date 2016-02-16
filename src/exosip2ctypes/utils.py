# -*- coding: utf-8 -*-

"""
Some helper functions
"""

import logging

__all__ = ['b2s', 's2b', 'LoggerMixin']


def b2s(s, encoding='utf-8'):
    """Ensure to get a `str` string

    Return original `s` if it is not a `str` string

    :param s: `unicode` or `bytes` string
    :type s: bytes or unicode
    :param str encoding: codec
    :return: `str` string, it's `bytes` in Python 2.x, `unicode` in Python3.x
    :rtype: str
    """
    if bytes != str:
        if isinstance(s, bytes):
            return s.decode(encoding)
    return s


def s2b(s, encoding='utf-8'):
    """Ensure to get a `bytes` string

    Return original `s` if it is not a `unicode` string

    :param unicode s: `unicode` or `bytes` string
    :param str encoding: codec
    :return: `bytes` string, it equals `bytes` in Python 2.x
    :rtype: bytes
    """
    if bytes != str:
        if isinstance(s, str):
            return s.encode(encoding)
    return s


class LoggerMixin:
    """Mixin Class provide a :attr:`logger` property
    """

    @property
    def logger(self):
        """`logger` instance.

        :rtype: logging.Logger

        logger name format is `ModuleName.ClassName`
        """
        try:
            name = '{0.__module__:s}.{0.__qualname__:s}'.format(self.__class__)
        except AttributeError:
            name = '{0.__module__:s}.{0.__name__:s}'.format(self.__class__)
        return logging.getLogger(name)
