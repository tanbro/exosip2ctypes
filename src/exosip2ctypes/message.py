# -*- coding: utf-8 -*-

from ctypes import POINTER, byref, string_at, create_string_buffer, c_void_p, c_char_p, c_int, c_size_t

from ._c import lib, osip_parser, osip_content_type, osip_from, osip_header, osip_content_length, osip_body
from .error import raise_if_osip_error
from .utils import to_str, to_bytes

__all__ = ['OsipMessage', 'ExosipMessage']


class OsipMessage(object):

    def __init__(self, ptr):
        """class for osip2 message API

        :param ctypes.c_void_p ptr: Pointer to the `osip_message_t` structure in C library
        """
        if not ptr:
            raise RuntimeError('Null pointer.')
        self._ptr = ptr

    def __str__(self):
        """Get a string representation of a osip_message_t element.

        :rtype: str
        """
        dest = c_char_p()
        length = c_size_t()
        error_code = osip_parser.FuncMessageToStr.c_func(
            self._ptr, byref(dest), byref(length))
        raise_if_osip_error(error_code)
        if not dest:
            return str(None)
        result = string_at(dest, length.value)
        result = to_str(result)
        lib.free(dest)
        return result

    @property
    def ptr(self):
        """Pointer to the `osip_message_t` C Structure

        :rtype: ctypes.c_void_p
        """
        return self._ptr

    @property
    def call_id(self):
        """Call-id header.

        :rtype: str
        """
        ret = osip_parser.FuncMessageGetCallId.c_func(self._ptr)
        result = ret.contents.number
        return to_str(result)

    @call_id.setter
    def call_id(self, val):
        buf = create_string_buffer(to_bytes(val))
        error_code = osip_parser.FuncMessageSetCallId.c_func(self._ptr, buf)
        raise_if_osip_error(error_code)

    @property
    def content_type(self):
        """Content Type string of the SIP message

        :rtype: str
        """
        head_ptr = osip_parser.FuncMessageGetContentType.c_func(self._ptr)
        if not head_ptr:
            return None
        dest = c_char_p()
        err_code = osip_content_type.FuncContentTypeToStr.c_func(
            head_ptr, byref(dest))
        raise_if_osip_error(err_code)
        if not dest:
            return None
        result = to_str(dest.value)
        lib.free(dest)
        return result.strip()

    @content_type.setter
    def content_type(self, val):
        buf = create_string_buffer(to_bytes(val))
        err_code = osip_parser.FuncMessageSetContentType.c_func(self._ptr, buf)
        raise_if_osip_error(err_code)

    @property
    def content_length(self):
        """Content-length header.

        :rtype: int
        """
        pdest = osip_parser.FuncMessageGetContentLength.c_func(self._ptr)
        if isinstance(pdest, (type(None), c_void_p)):
            return None
        return int(pdest.contents.value)

    @content_length.setter
    def content_length(self, val):
        val = int(val)
        if val < 0:
            raise ValueError(
                'Content-Length header value must be greater than or equal 0.')
        buf = create_string_buffer(to_bytes(str(val)))
        error_code = osip_parser.FuncMessageSetContentLength.c_func(
            self._ptr, buf)
        raise_if_osip_error(error_code)

    @property
    def from_(self):
        """From header

        :rtype: str
        """
        ptr = osip_parser.FuncMessageGetFrom.c_func(self._ptr)
        dest = c_char_p()
        error_code = osip_from.FuncFromToStr.c_func(ptr, byref(dest))
        raise_if_osip_error(error_code)
        if not dest:
            return None
        result = to_str(dest.value)
        lib.free(dest)
        return result.strip()

    @from_.setter
    def from_(self, val):
        buf = create_string_buffer(to_bytes(val))
        error_code = osip_parser.FuncMessageSetFrom.c_func(self._ptr, buf)
        raise_if_osip_error(error_code)

    @property
    def to(self):
        """To header.

        :rtype: str
        """
        ptr = osip_parser.FuncMessageGetTo.c_func(self._ptr)
        dest = c_char_p()
        error_code = osip_from.FuncFromToStr.c_func(ptr, byref(dest))
        raise_if_osip_error(error_code)
        if not dest:
            return None
        result = to_str(dest.value)
        lib.free(dest)
        return result.strip()

    @to.setter
    def to(self, val):
        buf = create_string_buffer(to_bytes(val))
        error_code = osip_parser.FuncMessageSetTo.c_func(self._ptr, buf)
        raise_if_osip_error(error_code)

    @property
    def contacts(self):
        """Get Contact header list.

        :rtype: list
        """
        result = []
        pos = 0
        while True:
            dest = c_void_p()
            found_pos = osip_parser.FuncMessageGetContact.c_func(
                self._ptr, c_int(pos), byref(dest))
            if int(found_pos) < 0:
                break
            pos = int(found_pos) + 1
            pch_contact = c_char_p()
            error_code = osip_from.FuncFromToStr.c_func(
                dest, byref(pch_contact))
            raise_if_osip_error(error_code)
            contact = to_str(pch_contact.value)
            lib.free(pch_contact)
            result.append(contact.strip())
        return result

    def add_contact(self, val):
        """Set the Contact header.

        :param str val: The string describing the element.

        .. attention:: This method will **ADD** a create `Contact` header
        """
        buf = create_string_buffer(to_bytes(val))
        error_code = osip_parser.FuncMessageSetContact.c_func(self._ptr, buf)
        raise_if_osip_error(error_code)

    @property
    def allows(self):
        """Get Allow header list.

        :rtype: list
        """
        result = []
        pos = 0
        while True:
            dest = POINTER(osip_content_length.Allow)()
            found_pos = osip_parser.FuncMessageGetAllow.c_func(
                self._ptr, c_int(pos), byref(dest))
            if int(found_pos) < 0:
                break
            pos = int(found_pos) + 1
            result.append(to_str(dest.contents.value))
        return result

    def add_allow(self, val):
        """Set the Allow header.

        :param str val: The string describing the element.

        .. attention:: This method will **ADD** a create `ALLOW` header
        """
        buf = create_string_buffer(to_bytes(val))
        error_code = osip_parser.FuncMessageSetAllow.c_func(self._ptr, buf)
        raise_if_osip_error(error_code)

    def get_headers(self, name):
        """Find "unknown" header's list. (not defined in oSIP)

        :param str name: The name of the header to find.
        :return: Header's value string list.
        :rtype: list
        """
        result = []
        pc_name = create_string_buffer(to_bytes(name))
        pos = 0
        while True:
            p_header = POINTER(osip_header.Header)()
            found_pos = osip_parser.FuncMessageHeaderGetByName.c_func(
                self._ptr,
                pc_name,
                c_int(pos),
                byref(p_header)
            )
            if int(found_pos) < 0:
                break
            pos = int(found_pos) + 1
            val = p_header.contents.hvalue
            result.append(to_str(val))
        return result

    def add_header(self, name, value):
        """Allocate and Add an "unknown" header (not defined in oSIP).

        :param str name: The token name.
        :param str value: The token value.

        .. attention:: This method will **ADD** a create header
        """
        pc_name = create_string_buffer(to_bytes(name))
        pc_value = create_string_buffer(to_bytes(value))
        error_code = osip_parser.FuncMessageSetHeader.c_func(
            self._ptr,
            pc_name,
            pc_value
        )
        raise_if_osip_error(error_code)

    @property
    def bodies(self):
        """Get body header list.

        :rtype: list
        """
        result = []
        pos = 0
        while True:
            p_body = c_void_p()
            found_pos = osip_parser.FuncMessageGetBody.c_func(
                self._ptr, c_int(pos), byref(p_body))
            if int(found_pos) < 0:
                break
            pos = int(found_pos) + 1
            dest = c_char_p()
            length = c_size_t()
            ret = osip_body.FuncBodyToStr.c_func(
                p_body, byref(dest), byref(length))
            raise_if_osip_error(ret)
            val = string_at(dest, length.value)
            val = to_str(val)
            lib.free(dest)
            result.append(val)
        return result

    def add_body(self, val):
        """Fill the body of message.

        :param str val: Body string.

        .. attention:: This method will **ADD** a create body
        """
        buf = create_string_buffer(to_bytes(val))
        err_code = osip_parser.FuncMessageSetBody.c_func(
            self._ptr, buf, len(buf))
        raise_if_osip_error(err_code)


class ExosipMessage(OsipMessage):

    def __init__(self, ptr, context):
        """class for eXosip2 message API

        :param ctypes.c_void_p ptr: Pointer to the `osip_message_t` structure in C library
        :param Context context: eXosip context

        .. danger:: Do **NOT** con/destruct the class yourself unless you known what you are doing.

        .. attention::
            In eXosip2, messages are managed inside the library,
            so we should **NOT** free :class:`OsipMessage` object manually.
        """
        if not context:
            raise RuntimeError('No context.')
        self._context = context
        super(ExosipMessage, self).__init__(ptr)

    def send(self):
        self._context.send_message(self)

    @property
    def context(self):
        """eXosip context of the message

        :rtype: Context
        """
        return self._context
