# -*- coding: utf-8 -*-

"""
eXosip2 SDP helper API.
"""

from ctypes import byref, create_string_buffer, string_at, c_char_p

from ._c import sdp
from .error import raise_if_osip_error
from .utils import b2s, s2b


class SdpMessage:
    def __init__(self, ptr):
        """SDP body

        :param ctypes.c_void_p ptr: `sdp_message_t*`
        """
        self._prt = ptr

    @property
    def ptr(self):
        return self._prt
