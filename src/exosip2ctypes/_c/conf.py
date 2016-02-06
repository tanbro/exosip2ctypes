# -*- coding: utf-8 -*-

"""
eXosip2 configuration API
"""

from ctypes import POINTER, c_int, c_void_p, c_char_p

from . import globs
from .utils import ExosipFunc


class FuncMalloc(ExosipFunc):
    func_name = 'malloc'
    restype = POINTER(c_void_p)


class FuncInit(ExosipFunc):
    func_name = 'init'
    argtypes = [c_void_p]
    restype = c_int


class FuncQuit(ExosipFunc):
    func_name = 'quit'
    argtypes = [c_void_p]


class FuncLock(ExosipFunc):
    func_name = 'lock'
    argtypes = [c_void_p]


class FuncUnlock(ExosipFunc):
    func_name = 'unlock'
    argtypes = [c_void_p]


class FuncListenAddr(ExosipFunc):
    func_name = 'listen_addr'
    argtypes = [c_void_p, c_int, c_char_p, c_int, c_int, c_int]
    restype = c_int


class FuncSetUserAgent(ExosipFunc):
    func_name = 'set_user_agent'
    argtypes = [c_void_p, c_char_p]


class FuncGetVersion(ExosipFunc):
    func_name = 'get_version'
    restype = c_char_p


class FuncSetOption(ExosipFunc):
    func_name = 'set_option'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_char_p


class FuncMasqueradeContact(ExosipFunc):
    func_name = 'masquerade_contact'
    argtypes = [c_void_p, c_char_p, c_int]


globs.func_classes.extend([
    FuncMalloc,
    FuncInit,
    FuncQuit,
    FuncLock,
    FuncUnlock,
    FuncListenAddr,
    FuncSetUserAgent,
    FuncGetVersion,
    FuncSetOption,
    FuncMasqueradeContact,
])
