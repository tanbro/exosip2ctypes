# -*- coding: utf-8 -*-

"""
eXosip call API

This file provide the API needed to control calls. You can use it to:

build initial invite.
send initial invite.
build request within the call.
send request within the call.
This API can be used to build the following messages:

   INVITE, INFO, OPTIONS, REFER, UPDATE, NOTIFY

"""

from ctypes import byref, c_void_p, c_int

from ._c import call
from .message import ExosipMessage
from .utils import raise_if_osip_error

__all__ = ['Answer']


class Ack(ExosipMessage):
    def __init__(self, context, did):
        ptr = c_void_p
        err_code = call.FuncCallBuildAck.c_func(context.ptr, int(did), byref(ptr))
        raise_if_osip_error(err_code)
        super(Answer, self).__init__(ptr, context)
        self._did = did

        @property
        def did(self):
            return self._did


class Answer(ExosipMessage):
    def __init__(self, context, tid, status):
        ptr = c_void_p()  # struct osip_message_t *p ===> void *p
        err_code = call.FuncCallBuildAnswer.c_func(context.ptr, c_int(tid), c_int(status), byref(ptr))
        raise_if_osip_error(err_code)
        super(Answer, self).__init__(ptr, context)
        self._tid = tid
        self._status = status

    @property
    def tid(self):
        return self._tid

    @property
    def status(self):
        return self._status
