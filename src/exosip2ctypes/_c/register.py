# -*- coding: utf-8 -*-

"""
eXosip2 REGISTER and Registration Management
"""

from ctypes import c_void_p, c_int, c_char_p

from . import globs
from .utils import ExosipFunc


class FuncRegisterBuildInitialRegister(ExosipFunc):
    """Build initial REGISTER request.

    To start a registration, you need to build a default REGISTER request by providing several mandatory headers.

    You can start as many registration you want even in one eXosip_t context.

    The returned element of eXosip_register_build_initial_register is the registration identifier that you can use to update your registration.
    In future events about this registration, you'll see that registration identifier when applicable.
    """
    func_name = 'register_build_initial_register'
    argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int, c_void_p]
    restype = c_int


class FuncRegisterBuildRegister(ExosipFunc):
    """Build a new REGISTER request for an existing registration."""
    func_name = 'register_build_register'
    argtypes = [c_void_p, c_int, c_int, c_void_p]
    restype = c_int


class FuncRegisterSendSegister(ExosipFunc):
    """Send a REGISTER request for an existing registration."""
    func_name = 'register_send_register'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_int


class FuncRegisterRemove(ExosipFunc):
    """Remove existing registration without sending REGISTER."""
    func_name = 'register_remove'
    argtypes = [c_void_p, c_int]
    restype = c_int


globs.func_classes.extend([
    FuncRegisterBuildInitialRegister,
    FuncRegisterBuildRegister,
    FuncRegisterSendSegister,
    FuncRegisterRemove,
])
