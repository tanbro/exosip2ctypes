# -*- coding: utf-8 -*-

"""
oSIP parser Handling
"""

from ctypes import POINTER, c_int, c_void_p, c_char_p, c_size_t

from . import globs
from .utils import OsipFunc

from .osip_call_id import CallId
from .osip_content_length import ContentLength, Allow
from .osip_header import Header


class FuncMessageToStr(OsipFunc):
    func_name = 'message_to_str'
    argtypes = [c_void_p, POINTER(c_char_p), POINTER(c_size_t)]


class FuncMessageGetBody(OsipFunc):
    func_name = 'message_get_body'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_int


class FuncMessageSetBody(OsipFunc):
    func_name = 'message_set_body'
    argtypes = [c_void_p, c_char_p, c_size_t]
    restype = c_int


class FuncMessageHeaderGetByName(OsipFunc):
    func_name = 'message_header_get_byname'
    argtypes = [c_void_p, c_char_p, c_int, POINTER(POINTER(Header))]
    restype = c_int


class FuncMessageSetHeader(OsipFunc):
    func_name = 'message_set_header'
    argtypes = [c_void_p, c_char_p, c_char_p]
    restype = c_int


class FuncMessageGetCallId(OsipFunc):
    func_name = 'message_get_call_id'
    argtypes = [c_void_p]
    restype = POINTER(CallId)


class FuncMessageSetCallId(OsipFunc):
    func_name = 'message_set_call_id'
    argtypes = [c_void_p, c_char_p]
    restype = c_int


class FuncMessageGetContentLength(OsipFunc):
    func_name = 'message_get_content_length'
    argtypes = [c_void_p]
    restype = POINTER(ContentLength)


class FuncMessageSetContentLength(OsipFunc):
    func_name = 'message_set_content_length'
    argtypes = [c_void_p, c_char_p]
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


class FuncMessageGetTo(OsipFunc):
    func_name = 'message_get_to'
    argtypes = [c_void_p]
    restype = c_void_p


class FuncMessageSetTo(OsipFunc):
    func_name = 'message_set_to'
    argtypes = [c_void_p, c_char_p]
    restype = c_int


class FuncMessageGetContact(OsipFunc):
    func_name = 'message_get_contact'
    argtypes = [c_void_p, c_int, c_void_p]
    restype = c_int


class FuncMessageSetContact(OsipFunc):
    func_name = 'message_set_contact'
    argtypes = [c_void_p, c_char_p]
    restype = c_int


class FuncMessageGetAllow(OsipFunc):
    func_name = 'message_get_allow'
    argtypes = [c_void_p, c_int, POINTER(POINTER(Allow))]
    restype = c_int


class FuncMessageSetAllow(OsipFunc):
    func_name = 'message_set_allow'
    argtypes = [c_void_p, c_char_p]
    restype = c_int


globs.func_classes.extend([
    FuncMessageToStr,
    FuncMessageGetBody,
    FuncMessageSetBody,
    FuncMessageHeaderGetByName,
    FuncMessageSetHeader,
    FuncMessageGetCallId,
    FuncMessageSetCallId,
    FuncMessageGetContentLength,
    FuncMessageSetContentLength,
    FuncMessageGetContentType,
    FuncMessageSetContentType,
    FuncMessageGetFrom,
    FuncMessageSetFrom,
    FuncMessageGetTo,
    FuncMessageSetTo,
    FuncMessageGetContact,
    FuncMessageSetContact,
    FuncMessageGetAllow,
    FuncMessageSetAllow,
])
