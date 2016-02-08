# -*- coding: utf-8 -*-

"""
Some helper functions
"""

__all__ = ['b2s', 's2b']


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
