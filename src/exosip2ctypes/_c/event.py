# -*- coding: utf-8 -*-

"""
eXosip2 event API
"""

from ctypes import POINTER, Structure, c_int, c_void_p, c_char

from . import globs
from .utils import ExosipFunc


class StructEvent(Structure):
    _fields_ = [
        ('type', c_int),
        ('textinfo', c_char * 256),
        ('external_reference', c_void_p),
        ('request', c_void_p),
        ('response', c_void_p),
        ('ack', c_void_p),
        ('tid', c_int),
        ('did', c_int),
        ('rid', c_int),
        ('cid', c_int),
        ('sid', c_int),
        ('nid', c_int),
        ('ss_status', c_int),
        ('ss_reason', c_int),
    ]


class FuncEventWait(ExosipFunc):
    func_name = 'event_wait'
    argtypes = [c_void_p, c_int, c_int]
    restype = POINTER(StructEvent)


class FuncEventFree(ExosipFunc):
    func_name = 'event_free'
    argtypes = [c_void_p]


globs.func_classes.extend([
    FuncEventWait,
    FuncEventFree,
])
