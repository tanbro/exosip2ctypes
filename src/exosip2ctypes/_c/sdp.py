# -*- coding: utf-8 -*-

"""
eXosip2 SDP helper API.
"""

from ctypes import c_int, c_void_p

from . import globs
from .utils import ExosipFunc


class FuncGetRemoteSdp(ExosipFunc):
    func_name = 'get_remote_sdp'
    argtypes = [c_void_p, c_int]
    restype = c_void_p


globs.func_classes.extend([

])
