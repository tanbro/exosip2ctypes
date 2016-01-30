# -*- coding: utf-8 -*-

"""
eX_message.h
"""

from ctypes import c_int, c_void_p, c_char_p

from . import globs
from .utils import ExosipFunc


class FuncMessageBuildRequest(ExosipFunc):
    func_name = 'message_build_request'
    argtypes = [c_void_p, c_void_p, c_char_p, c_void_p, c_char_p, c_void_p]
    restype = c_int


class FuncMessageSendRequest(ExosipFunc):
    func_name = 'message_send_request'
    argtypes = [c_void_p, c_void_p]
    restype = c_int


class FuncMessageBuildAnswer(ExosipFunc):
    func_name = 'message_build_answer'
    argtypes = [c_void_p, c_int, c_int, c_void_p]
    restype = c_int


class FuncMessageSendAnswer(ExosipFunc):
    func_name = 'message_send_answer'
    argtypes = [c_void_p, c_int, c_int, c_void_p]
    restype = c_int


globs.func_classes.extend([
    FuncMessageBuildRequest,
    FuncMessageSendRequest,
    FuncMessageBuildAnswer,
    FuncMessageSendAnswer,
])
