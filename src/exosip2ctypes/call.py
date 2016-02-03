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

from ctypes import byref, c_void_p

from ._c import call
from .message import Message
from .utils import raise_if_not_zero

__all__ = ['AnswerMessage']


class AnswerMessage(Message):
    def __init__(self, tid, status):
        ptr = c_void_p()  # struct osip_message_t *p ===> void *p
        err_code = call.FuncCallBuildAnswer.c_func(int(tid), int(status), byref(ptr))
        raise_if_not_zero(err_code)
        self._tid = tid
        self._status = status
        super().__init__(ptr)

    @property
    def tid(self):
        return self._tid

    @property
    def status(self):
        return self._status
