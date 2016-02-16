# -*- coding: utf-8 -*-

from ctypes import POINTER, byref, create_string_buffer, string_at, c_void_p, c_char_p, c_int, c_size_t

from ._c import lib, osip_parser, osip_content_type, osip_from, osip_header, osip_content_length
from .error import raise_if_osip_error
from .utils import to_str, to_bytes


class OsipMessage:
    def __init__(self, ptr):
        """class for osip2 message API

        :param ctypes.c_void_p ptr: Pointer to the `osip_message_t` structure in C library
        """
        self._ptr = ptr

    def __str__(self):
        """Get a string representation of a osip_message_t element.

        :rtype: str
        """
        dest = c_char_p()
        message_length = c_size_t()
        error_code = osip_parser.FuncMessageToStr.c_func(self._ptr, byref(dest), byref(message_length))
        raise_if_osip_error(error_code)
        if not dest:
            return None
        result = string_at(dest)
        lib.free(dest)
        return to_str(result)

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
        err_code = osip_content_type.FuncContentTypeToStr.c_func(head_ptr, byref(dest))
        raise_if_osip_error(err_code)
        if not dest:
            return None
        result = string_at(dest)
        lib.free(dest)
        return to_str(result)

    @content_type.setter
    def content_type(self, val):
        buf = create_string_buffer(to_bytes(val))
        err_code = osip_parser.FuncMessageSetContentType.c_func(self._ptr, buf)
        raise_if_osip_error(err_code)

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
        result = string_at(dest)
        lib.free(dest)
        return to_str(result)

    @from_.setter
    def from_(self, val):
        buf = create_string_buffer(to_bytes(val))
        error_code = osip_parser.FuncMessageSetFrom.c_func(self._ptr, buf)
        raise_if_osip_error(error_code)

    @property
    def contacts(self):
        """Contact header list.

        :rtype: list
        """
        result = []
        pos = ret = 0
        while True:
            dest = c_void_p()
            ret = osip_parser.FuncMessageGetContact.c_func(self._ptr, c_int(pos), byref(dest))
            if int(ret) < 0:
                break
            pch_contact = c_char_p()
            error_code = osip_from.FuncFromToStr.c_func(dest, byref(pch_contact))
            raise_if_osip_error(error_code)
            contact = string_at(pch_contact)
            lib.free(pch_contact)
            result.append(to_str(contact))
            pos += 1
        return result

    @contacts.setter
    def contacts(self, val):
        contacts_str = ','.join(val)
        buf = create_string_buffer(to_bytes(contacts_str))
        error_code = osip_parser.FuncMessageSetContact.c_func(self._ptr, buf)
        raise_if_osip_error(error_code)

    @property
    def allows(self):
        """Allow header list.

        :rtype: list
        """
        result = []
        pos = ret = 0
        while True:
            dest = POINTER(osip_content_length.Allow)()
            ret = osip_parser.FuncMessageGetAllow.c_func(self._ptr, c_int(pos), byref(dest))
            if int(ret) < 0:
                break
            result.append(to_str(dest.contents.value))
            pos += 1
        return result

    @allows.setter
    def allows(self, val):
        allows_str = ', '.join(val)
        buf = create_string_buffer(to_bytes(allows_str))
        error_code = osip_parser.FuncMessageSetAllow.c_func(self._ptr, buf)
        raise_if_osip_error(error_code)

    def get_header(self, name, pos=0):
        """Find an "unknown" header. (not defined in oSIP)

        :param str name: The name of the header to find.
        :param int pos: The index where to start searching for the header.
        :return: header's value string
        :rtype: str
        :raises KeyError: if header name not found
        """
        pc_name = create_string_buffer(to_bytes(name))
        p_header = POINTER(osip_header.Header)()
        found_pos = osip_parser.FuncMessageHeaderGetByName.c_func(
            self._ptr,
            pc_name,
            c_int(pos),
            byref(p_header)
        )
        if found_pos < 0:
            raise KeyError('Header by name "{}" can not be found in the SIP message'.format(name))
        value = p_header.contents.hvalue
        return to_str(value)

    def set_header(self, name, value):
        """Allocate and Add an "unknown" header (not defined in oSIP).

        :param str name: The token name.
        :param str value: The token value.
        """
        pc_name = create_string_buffer(to_bytes(name))
        pc_value = create_string_buffer(to_bytes(value))
        error_code = osip_parser.FuncMessageSetHeader.c_func(
            self._ptr,
            pc_name,
            pc_value
        )
        raise_if_osip_error(error_code)

    def set_body(self, val):
        """Fill the body of message.

        :param str val: Body string.
        """
        buf = create_string_buffer(to_bytes(val))
        err_code = osip_parser.FuncMessageSetBody.c_func(self._ptr, buf, len(buf))
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
