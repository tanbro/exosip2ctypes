# -*- coding: utf-8 -*-

"""
eXosip2 REGISTER and Registration Management
"""

from ctypes import c_void_p, c_int, c_char_p

from . import globs
from .utils import ExosipFunc


class RegisterBuildInitialRegister(ExosipFunc):
    """Build initial REGISTER request."""
    func_name = 'register_build_initial_register'
    argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int, c_void_p]
    restype = c_int


class RegisterBuildRegister(ExosipFunc):
    """Build a new REGISTER request for an existing registration."""
    func_name = 'register_build_register'
    argtypes = [c_void_p, c_int, c_int, c_void_p]
    restype = c_int


class RegisterSendSegister(ExosipFunc):
    """Send a REGISTER request for an existing registration."""
    func_name = 'register_send_register'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_int


class RegisterRemove(ExosipFunc):
    """Remove existing registration without sending REGISTER."""
    func_name = 'register_remove'
    argtypes = [c_void_p, c_int]
    restype = c_int


globs.func_classes.extend([
    RegisterBuildInitialRegister,
    RegisterBuildRegister,
    RegisterSendSegister,
    RegisterRemove,
])
