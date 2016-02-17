"""
oSIP body API.
"""

from ctypes import POINTER, c_int, c_void_p, c_char_p, c_size_t

from . import globs
from .utils import OsipFunc


class FuncBodyToStr(OsipFunc):
    func_name = 'body_to_str'
    argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t)]
    restype = c_int


globs.func_classes.extend([
    FuncBodyToStr,
])
