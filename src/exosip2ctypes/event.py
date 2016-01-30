# -*- coding: utf-8 -*-

"""
eXosip2 event API
"""

from enum import IntEnum

from ._c import event


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
    def __init__(self, p):
        self._p = p
        self.type = EventType(int(self._p.contents.type))

    def __del__(self):
        self.dispose()

    def dispose(self):
        if self._p:
            event.FuncEventFree.c_func(self._p)
            self._p = None

    @property
    def tid(self):
        return int(self._p.contents.tid)

    @property
    def did(self):
        return int(self._p.contents.did)

    @property
    def rid(self):
        return int(self._p.contents.rid)

    @property
    def cid(self):
        return int(self._p.contents.cid)

    @property
    def sid(self):
        return int(self._p.contents.sid)

    @property
    def nid(self):
        return int(self._p.contents.nid)

    @property
    def ss_status(self):
        return int(self._p.contents.ss_status)

    @property
    def ss_reason(self):
        return int(self._p.contents.ss_reason)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()
