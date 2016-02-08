# -*- coding: utf-8 -*-

from ctypes import POINTER, byref, create_string_buffer, string_at, c_void_p, c_char_p, c_int

from ._c import osip_parser, osip_content_type, osip_from, osip_header
from .error import raise_if_osip_error
from .utils import b2s, s2b


class OsipMessage:
    def __init__(self, ptr):
        """class for osip2 message API

        :param c_void_p ptr: Pointer to the `osip_message_t` structure in C library

        .. danger:: **Do NOT** con/destruct the class yourself unless you known what you are doing.

        .. attention:: in eXosip2, messages are managed by the library, so we should NOT free the messages manuall
        """
        self._ptr = ptr

    @property
    def ptr(self):
        return self._ptr

    @property
    def content_type(self):
        """Content Type string of the SIP message

        :type: str

        .. warning:: memory leak on setter!!!
        """
        head_ptr = osip_parser.FuncMessageGetContentType.c_func(self._ptr)
        if not head_ptr:
            return None
        pch = c_char_p()  # TODO: fix the memory leak!!!
        err_code = osip_content_type.FuncContentTypeToStr.c_func(head_ptr, byref(pch))
        raise_if_osip_error(err_code)
        if not pch:
            return None
        result = string_at(pch)
        del pch
        return b2s(result)

    @content_type.setter
    def content_type(self, val):
        buf = create_string_buffer(s2b(val))
        err_code = osip_parser.FuncMessageSetContentType.c_func(self._ptr, buf)
        raise_if_osip_error(err_code)

    @property
    def from_(self):
        """From header

        :rtype: str
        """
        ptr = osip_parser.FuncMessageGetFrom.c_func(self._ptr)
        pch = c_char_p()
        error_code = osip_from.FuncFromToStr.c_func(ptr, byref(pch))
        raise_if_osip_error(error_code)
        if not pch:
            return None
        result = string_at(pch)
        del pch
        return b2s(result)

    @from_.setter
    def from_(self, val):
        buf = create_string_buffer(s2b(val))
        error_code = osip_parser.FuncMessageSetFrom.c_func(self._ptr, buf)

    def get_header(self, name, pos=0):
        """Find an "unknown" header. (not defined in oSIP)

        :param str name: The name of the header to find.
        :param pos: The index where to start searching for the header.
        :return: header's value string
        :rtype: str
        :raises KeyError: if header name not found
        """
        pc_name = create_string_buffer(s2b(name))
        p_header = POINTER(osip_header.Header)()
        found_pos = osip_parser.FuncMessageHeaderGetByName.c_func(
            self._ptr,
            pc_name,
            c_int(pos),
            byref(p_header),
        )
        if found_pos < 0:
            raise KeyError('Header by name "{}" can not be found in the SIP message'.format(name))
        value = p_header.contents.hvalue
        return b2s(value)

    def set_body(self, val):
        buf = create_string_buffer(s2b(val))
        err_code = osip_parser.FuncMessageSetBody.c_func(self._ptr, buf, len(buf))
        raise_if_osip_error(err_code)


class ExosipMessage(OsipMessage):
    def __init__(self, ptr, context):
        """class for eXosip2 message API

        :param c_void_p ptr: Pointer to the `osip_message_t` structure in C library
        :param Context context: eXosip context

        .. danger:: **Do NOT** con/destruct the class yourself unless you known what you are doing.
        """
        self._context = context
        super(ExosipMessage, self).__init__(ptr)

    def send(self):
        self._context.send_message(self)

    @property
    def context(self):
        """
        :return: eXosip context of the message
        :rtype: Context
        """
        return self._context
