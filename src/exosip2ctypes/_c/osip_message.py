# -*- coding: utf-8 -*-

"""
oSIP SIP Message Accessor Routines
"""

from ctypes import c_int, c_void_p, c_char_p, c_size_t

from . import globs
from .utils import OsipFunc


class FuncMessageInit(OsipFunc):
    func_name = 'message_init'
    argtypes = [c_void_p]
    restype = c_int


class FuncMessageFree(OsipFunc):
    func_name = 'message_free'
    argtypes = [c_void_p]


class FuncMessageSetBody(OsipFunc):
    func_name = 'message_set_body'
    argtypes = [c_void_p, c_char_p, c_size_t]
    restype = c_int


class FuncMessageGetContentType(OsipFunc):
    func_name = 'message_get_content_type'
    argtypes = [c_void_p]
    restype = c_void_p


class FuncMessageSetContentType(OsipFunc):
    func_name = 'message_set_content_type'
    argtypes = [c_void_p, c_char_p]
    restype = c_int


globs.func_classes.extend([
    FuncMessageInit,
    FuncMessageFree,
    FuncMessageSetBody,
    FuncMessageGetContentType,
    FuncMessageSetContentType,
])
