# -*- coding: utf-8 -*-

"""
eXosip2 INVITE and Call Management
"""

from ctypes import c_int, c_void_p, c_char_p, c_size_t

from . import globs
from .utils import ExosipFunc


class FuncCallSetReference(ExosipFunc):
    func_name = 'call_set_reference'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_int


class FuncCallGetReference(ExosipFunc):
    func_name = 'call_get_reference'
    argtypes = [c_void_p, c_int]
    restype = c_void_p


class FuncCallBuildInitialInvite(ExosipFunc):
    func_name = 'call_build_initial_invite'
    argtypes = [c_void_p, c_void_p, c_char_p, c_char_p, c_char_p, c_char_p]
    restype = c_int


class FuncCallSendInitialInvite(ExosipFunc):
    func_name = 'call_send_initial_invite'
    argtypes = [c_void_p, c_void_p]
    restype = c_int


class FuncCallBuildRequest(ExosipFunc):
    func_name = 'call_build_request'
    argtypes = [c_void_p, c_int, c_char_p, c_void_p]
    restype = c_int


class FuncCallBuildAck(ExosipFunc):
    func_name = 'call_build_ack'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_int


class FuncCallSendAck(ExosipFunc):
    func_name = 'call_send_ack'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_int


class FuncCallBuildRefer(ExosipFunc):
    func_name = 'call_build_refer'
    argtypes = [c_void_p, c_int, c_void_p, c_void_p]
    restype = c_int


class FuncCallBuildInfo(ExosipFunc):
    func_name = 'call_build_info'
    argtypes = [c_void_p, c_int, c_void_p]
    restypes = c_int


class FuncCallBuildOptions(ExosipFunc):
    func_name = 'call_build_options'
    argtypes = [c_void_p, c_int, c_void_p]
    restypes = c_int


class FuncCallBuildUpdate(ExosipFunc):
    func_name = 'call_build_update'
    argtypes = [c_void_p, c_int, c_void_p]
    restypes = c_int


class FuncCallBuildNotify(ExosipFunc):
    func_name = 'call_build_notify'
    argtypes = [c_void_p, c_int, c_int, c_void_p]
    restype = c_int


class FuncCallSendRequest(ExosipFunc):
    func_name = 'call_send_request'
    argtypes = [c_void_p, c_int, c_int]
    restype = c_int


class FuncCallBuildAnswer(ExosipFunc):
    func_name = 'call_build_answer'
    argtypes = [c_void_p, c_int, c_int, c_void_p]
    restype = c_int


class FuncCallSendAnswer(ExosipFunc):
    func_name = 'call_send_answer'
    argtypes = [c_void_p, c_int, c_int, c_void_p]
    restype = c_int


class FuncCallTerminate(ExosipFunc):
    func_name = 'call_terminate'
    argtypes = [c_void_p, c_int, c_int]
    restype = c_int


# Only available in 4.10 and above
# class FuncCallTerminateWithReason(ExosipFunc):
#     func_name = 'call_terminate_with_reason'
#     argtypes = [c_void_p, c_int, c_int, c_char_p]
#     restype = c_int


class FuncCallBuildPrack(ExosipFunc):
    func_name = 'call_build_prack'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_int


class FuncCallSendPrack(ExosipFunc):
    func_name = 'call_send_prack'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_int


class FuncCallGetReferto(ExosipFunc):
    func_name = 'call_get_referto'
    argtypes = [c_void_p, c_int, c_char_p, c_size_t]
    restype = c_int


class FuncCallFindByReplaces(ExosipFunc):
    func_name = 'call_find_by_replaces'
    argtypes = [c_void_p, c_char_p]
    restype = c_int


globs.func_classes.extend([
    FuncCallSetReference,
    FuncCallGetReference,
    FuncCallBuildInitialInvite,
    FuncCallSendInitialInvite,
    FuncCallBuildRequest,
    FuncCallBuildAck,
    FuncCallSendAck,
    FuncCallBuildRefer,
    FuncCallBuildInfo,
    FuncCallBuildOptions,
    FuncCallBuildUpdate,
    FuncCallBuildNotify,
    FuncCallSendRequest,
    FuncCallBuildAnswer,
    FuncCallSendAnswer,
    FuncCallTerminate,
    # FuncCallTerminateWithReason, # Only available in 4.10 and above
    FuncCallBuildPrack,
    FuncCallSendPrack,
    FuncCallGetReferto,
    FuncCallFindByReplaces
])
