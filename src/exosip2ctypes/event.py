# -*- coding: utf-8 -*-

"""
eXosip2 event API
"""

from enum import IntEnum

from ._c import event

__all__ = ['EventType', 'Event']


class EventType(IntEnum):
    REGISTRATION_SUCCESS = 0
    REGISTRATION_FAILURE = 1
    CALL_INVITE = 2
    CALL_REINVITE = 3
    CALL_NOANSWER = 4
    CALL_PROCEEDING = 5
    CALL_RINGING = 6
    CALL_ANSWERED = 7
    CALL_REDIRECTED = 8
    CALL_REQUESTFAILURE = 9
    CALL_SERVERFAILURE = 10
    CALL_GLOBALFAILURE = 11
    CALL_ACK = 12
    CALL_CANCELLED = 13
    CALL_MESSAGE_NEW = 14
    CALL_MESSAGE_PROCEEDING = 15
    CALL_MESSAGE_ANSWERED = 16
    CALL_MESSAGE_REDIRECTED = 17
    CALL_MESSAGE_REQUESTFAILURE = 18
    CALL_MESSAGE_SERVERFAILURE = 19
    CALL_MESSAGE_GLOBALFAILURE = 20
    CALL_CLOSED = 21
    CALL_RELEASED = 22
    MESSAGE_NEW = 23
    MESSAGE_PROCEEDING = 24
    MESSAGE_ANSWERED = 25
    MESSAGE_REDIRECTED = 26
    MESSAGE_REQUESTFAILURE = 27
    MESSAGE_SERVERFAILURE = 28
    MESSAGE_GLOBALFAILURE = 29
    SUBSCRIPTION_NOANSWER = 30
    SUBSCRIPTION_PROCEEDING = 31
    SUBSCRIPTION_ANSWERED = 32
    SUBSCRIPTION_REDIRECTED = 33
    SUBSCRIPTION_REQUESTFAILURE = 34
    SUBSCRIPTION_SERVERFAILURE = 35
    SUBSCRIPTION_GLOBALFAILURE = 36
    SUBSCRIPTION_NOTIFY = 37
    IN_SUBSCRIPTION_NEW = 38
    NOTIFICATION_NOANSWER = 39
    NOTIFICATION_PROCEEDING = 40
    NOTIFICATION_ANSWERED = 41
    NOTIFICATION_REDIRECTED = 42
    NOTIFICATION_REQUESTFAILURE = 43
    NOTIFICATION_SERVERFAILURE = 44
    NOTIFICATION_GLOBALFAILURE = 45
    EVENT_COUNT = 46


class Event:
    def __init__(self, pointer):
        self._pointer = pointer
        self._type = EventType(int(pointer.contents.type))
        self._tid = int(pointer.contents.tid)
        self._did = int(pointer.contents.did)
        self._rid = int(pointer.contents.rid)
        self._cid = int(pointer.contents.cid)
        self._sid = int(pointer.contents.sid)
        self._nid = int(pointer.contents.nid)
        self._ss_status = int(pointer.contents.ss_status)
        self._ss_reason = int(pointer.contents.ss_reason)

    def __del__(self):
        self.dispose()

    def dispose(self):
        if self._pointer:
            event.FuncEventFree.c_func(self._pointer)
            self._pointer = None

    @property
    def type(self):
        return self._type

    @property
    def tid(self):
        return self._tid

    @property
    def did(self):
        return self._did

    @property
    def rid(self):
        return self._rid

    @property
    def cid(self):
        return self._cid

    @property
    def sid(self):
        return self._sid

    @property
    def nid(self):
        return self._nid

    @property
    def ss_status(self):
        return self._ss_status

    @property
    def ss_reason(self):
        return self._ss_reason

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()
