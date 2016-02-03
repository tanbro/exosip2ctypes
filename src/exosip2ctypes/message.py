# -*- coding: utf-8 -*-

from ctypes import byref, create_string_buffer, string_at, c_char_p

from ._c import osip_message, osip_content_type
from .utils import raise_if_not_zero


class Message:
    """
    class for osip2 message API
    """

    def __init__(self, ptr):
        self._ptr = ptr

    def __del__(self):
        self.dispose()

    def dispose(self):
        if self._ptr:
            osip_message.FuncMessageFree.c_func(self._ptr)
            self._ptr = None

    @property
    def ptr(self):
        return self._ptr

    @property
    def content_type(self):
        """
        .. warning:: memory leak!!!
        """
        head_ptr = osip_message.FuncMessageGetContentType.c_func(self._ptr)
        if not head_ptr:
            return None
        pch = c_char_p()  # todo: fix the memory leak!!!
        err_code = osip_content_type.FuncContentTypeToStr.c_func(head_ptr, byref(pch))
        raise_if_not_zero(err_code)
        if not pch:
            return None
        result = string_at(pch)
        del pch
        return result if isinstance(result, str) else result.decode()

    @content_type.setter
    def content_type(self, val):
        buf = create_string_buffer(val.encode())
        err_code = osip_message.FuncMessageSetBody.c_func(self._ptr, byref(buf), len(buf))
        raise_if_not_zero(err_code)
