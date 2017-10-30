# -*- coding: utf-8 -*-

"""
eXosip2 SDP helper API.
"""

from __future__ import absolute_import, unicode_literals

__all__ = ['SdpMessage']


class SdpMessage(object):

    def __init__(self, ptr):
        """SDP body

        :param ctypes.c_void_p ptr: `sdp_message_t*`
        """
        self._prt = ptr

    @property
    def ptr(self):
        return self._prt
