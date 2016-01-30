# -*- coding: utf-8 -*-

"""
eXosip2 authentication API
"""

from ctypes import POINTER, c_byte, c_int, c_void_p, CFUNCTYPE, c_char_p, c_ushort, c_long

from . import globs
from .utils import ExosipFunc


class FuncAutomaticAction(ExosipFunc):
    func_name = 'automatic_action'
    argtypes = [c_void_p]


globs.func_classes.extend([
    FuncAutomaticAction,
])
