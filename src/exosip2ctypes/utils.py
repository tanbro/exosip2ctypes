# -*- coding: utf-8 -*-

"""
some helper functions
"""

__all__ = ['b2s', 's2b']


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
