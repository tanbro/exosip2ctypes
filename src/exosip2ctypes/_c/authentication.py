# -*- coding: utf-8 -*-

"""
eXosip2 authentication API
"""

from ctypes import c_int, c_void_p, c_char_p

from . import globs
from .utils import ExosipFunc


class FuncAutomaticAction(ExosipFunc):
    func_name = 'automatic_action'
    argtypes = [c_void_p]


class FuncAddAuthenticationInfo(ExosipFunc):
    func_name = 'add_authentication_info'
    argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]
    restype = c_int


class FuncRemoveAuthenticationInfo(ExosipFunc):
    func_name = 'remove_authentication_info'
    argtypes = [c_void_p, c_char_p, c_char_p]
    restype = c_int


class FuncClearAuthenticationInfo(ExosipFunc):
    func_name = 'clear_authentication_info'
    argtypes = [c_void_p]
    restype = c_int


globs.func_classes.extend([
    FuncAutomaticAction,
    FuncAddAuthenticationInfo,
    FuncRemoveAuthenticationInfo,
    FuncClearAuthenticationInfo,
])
