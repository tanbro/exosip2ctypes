"""
oSIP from header definition.
"""

from ctypes import POINTER, c_int, c_void_p, c_char_p

from . import globs
from .utils import OsipFunc


class FuncFromToStr(OsipFunc):
    func_name = 'from_to_str'
    argtypes = [c_void_p, POINTER(c_char_p)]
    restype = c_int


globs.func_classes.extend([
    FuncFromToStr,
])
