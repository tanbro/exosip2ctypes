# -*- coding: utf-8 -*-

from ctypes import POINTER, byref, create_string_buffer, string_at, c_char_p

from ._c import osip_message, osip_content_type
from .utils import raise_if_not_zero


class Message:
    """
    class for osip2 message API
    """

    def __init__(self, pointer):
        self._pointer = pointer

    def __del__(self):
        self.dispose()

    def dispose(self):
        if self._pointer:
            osip_message.FuncMessageFree.c_func(self._pointer)
            self._pointer = None

    @property
    def pointer(self):
        return self._pointer

    @property
    def content_type(self):
        """
        .. warning:: memory leak!!!
        """
        p_head = osip_message.FuncMessageGetContentType.c_func(self._pointer)
        if not p_head:
            return None
        p = c_char_p()  # todo: fix the memory leak!!!
        err_code = osip_content_type.FuncContentTypeToStr.c_func(p_head, byref(p))
        raise_if_not_zero(err_code)
        if not p:
            return None
        result = string_at(p)
        return result if isinstance(result, str) else result.decode()

    @content_type.setter
    def content_type(self, val):
        buf = create_string_buffer(val.encode())
        err_code = osip_message.FuncMessageSetBody.c_func(self._pointer, byref(buf), len(buf))
        raise_if_not_zero(err_code)
