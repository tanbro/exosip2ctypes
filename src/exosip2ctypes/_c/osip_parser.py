# -*- coding: utf-8 -*-

"""
oSIP parser Handling
"""

from ctypes import POINTER, c_int, c_void_p, c_char_p, c_size_t

from . import globs
from .utils import OsipFunc

from .osip_header import Header


class FuncMessageSetBody(OsipFunc):
    func_name = 'message_set_body'
    argtypes = [c_void_p, c_char_p, c_size_t]
    restype = c_int


class FuncMessageHeaderGetByName(OsipFunc):
    func_name = 'message_header_get_byname'
    argtypes = [c_void_p, c_char_p, c_int, POINTER(POINTER(Header))]
    restype = c_int


class FuncMessageGetContentType(OsipFunc):
    func_name = 'message_get_content_type'
    argtypes = [c_void_p]
    restype = c_void_p


class FuncMessageSetContentType(OsipFunc):
    func_name = 'message_set_content_type'
    argtypes = [c_void_p, c_char_p]
    restype = c_int


class FuncMessageGetFrom(OsipFunc):
    func_name = 'message_get_from'
    argtypes = [c_void_p]
    restype = c_void_p


class FuncMessageSetFrom(OsipFunc):
    func_name = 'message_set_from'
    argtypes = [c_void_p, c_char_p]
    restype = c_int


globs.func_classes.extend([
    FuncMessageSetBody,
    FuncMessageHeaderGetByName,
    FuncMessageGetContentType,
    FuncMessageSetContentType,
    FuncMessageGetFrom,
    FuncMessageSetFrom,
])
