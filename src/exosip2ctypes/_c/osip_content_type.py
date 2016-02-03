# -*- coding: utf-8 -*-

"""
oSIP content-type header definition.
"""

from ctypes import POINTER, c_void_p, c_int, c_char_p

from . import globs
from .utils import OsipFunc


class FuncContentTypeToStr(OsipFunc):
    func_name = 'content_type_to_str'
    argtypes = [c_void_p, POINTER(c_char_p)]
    restype = c_int


globs.func_classes.extend([
    FuncContentTypeToStr,
])
