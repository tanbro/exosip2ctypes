# -*- coding: utf-8 -*-

"""
eXosip2 event API
"""

from enum import IntEnum

from ._c import event

__all__ = ['EventType', 'Event']


class EventType(IntEnum):
    registration_success = event.EXOSIP_REGISTRATION_SUCCESS
    registration_failure = event.EXOSIP_REGISTRATION_FAILURE
    call_invite = event.EXOSIP_CALL_INVITE
    call_reinvite = event.EXOSIP_CALL_REINVITE
    call_noanswer = event.EXOSIP_CALL_NOANSWER
    call_proceeding = event.EXOSIP_CALL_PROCEEDING
    call_ringing = event.EXOSIP_CALL_RINGING
    call_answered = event.EXOSIP_CALL_ANSWERED
    call_redirected = event.EXOSIP_CALL_REDIRECTED
    call_requestfailure = event.EXOSIP_CALL_REQUESTFAILURE
    call_serverfailure = event.EXOSIP_CALL_SERVERFAILURE
    call_globalfailure = event.EXOSIP_CALL_GLOBALFAILURE
    call_ack = event.EXOSIP_CALL_ACK
    call_cancelled = event.EXOSIP_CALL_CANCELLED
    call_message_new = event.EXOSIP_CALL_MESSAGE_NEW
    call_message_proceeding = event.EXOSIP_CALL_MESSAGE_PROCEEDING
    call_message_answered = event.EXOSIP_CALL_MESSAGE_ANSWERED
    call_message_redirected = event.EXOSIP_CALL_MESSAGE_REDIRECTED
    call_message_requestfailure = event.EXOSIP_CALL_MESSAGE_REQUESTFAILURE
    call_message_serverfailure = event.EXOSIP_CALL_MESSAGE_SERVERFAILURE
    call_message_globalfailure = event.EXOSIP_CALL_MESSAGE_GLOBALFAILURE
    call_closed = event.EXOSIP_CALL_CLOSED
    call_released = event.EXOSIP_CALL_RELEASED
    message_new = event.EXOSIP_MESSAGE_NEW
    message_proceeding = event.EXOSIP_MESSAGE_PROCEEDING
    message_answered = event.EXOSIP_MESSAGE_ANSWERED
    message_redirected = event.EXOSIP_MESSAGE_REDIRECTED
    message_requestfailure = event.EXOSIP_MESSAGE_REQUESTFAILURE
    message_serverfailure = event.EXOSIP_MESSAGE_SERVERFAILURE
    message_globalfailure = event.EXOSIP_MESSAGE_GLOBALFAILURE
    subscription_noanswer = event.EXOSIP_SUBSCRIPTION_NOANSWER
    subscription_proceeding = event.EXOSIP_SUBSCRIPTION_PROCEEDING
    subscription_answered = event.EXOSIP_SUBSCRIPTION_ANSWERED
    subscription_redirected = event.EXOSIP_SUBSCRIPTION_REDIRECTED
    subscription_requestfailure = event.EXOSIP_SUBSCRIPTION_REQUESTFAILURE
    subscription_serverfailure = event.EXOSIP_SUBSCRIPTION_SERVERFAILURE
    subscription_globalfailure = event.EXOSIP_SUBSCRIPTION_GLOBALFAILURE
    subscription_notify = event.EXOSIP_SUBSCRIPTION_NOTIFY
    in_subscription_new = event.EXOSIP_IN_SUBSCRIPTION_NEW
    notification_noanswer = event.EXOSIP_NOTIFICATION_NOANSWER
    notification_proceeding = event.EXOSIP_NOTIFICATION_PROCEEDING
    notification_answered = event.EXOSIP_NOTIFICATION_ANSWERED
    notification_redirected = event.EXOSIP_NOTIFICATION_REDIRECTED
    notification_requestfailure = event.EXOSIP_NOTIFICATION_REQUESTFAILURE
    notification_serverfailure = event.EXOSIP_NOTIFICATION_SERVERFAILURE
    notification_globalfailure = event.EXOSIP_NOTIFICATION_GLOBALFAILURE
    # event_count = event.EXOSIP_EVENT_COUNT


class Event:
    def __init__(self, ptr):
        """
        :param ptr: pointer to the `eXosip_event_t` C structure allocated in C API `eXosip_event_wait()`
        :type ptr: exosip2ctypes._c.event.Event*
        """
        self._ptr = ptr
        self._type = EventType(int(ptr.contents.type))
        self._tid = int(ptr.contents.tid)
        self._did = int(ptr.contents.did)
        self._rid = int(ptr.contents.rid)
        self._cid = int(ptr.contents.cid)
        self._sid = int(ptr.contents.sid)
        self._nid = int(ptr.contents.nid)
        self._ss_status = int(ptr.contents.ss_status)
        self._ss_reason = int(ptr.contents.ss_reason)

    def __del__(self):
        self.dispose()

    def dispose(self):
        """free the `eXosip_event_t` C Structure allocated in C API `eXosip_event_wait()`

        ..attention::

            cause `libeXosip2` would not manage the event structure automatic, we shall free it manually!
            The memory free action is done in :class:`Event` 's destruction.
            so you can either `del` the event object or using the `with` statement,
            python's GC will free memory when the object is to free.
        """
        if self._ptr:
            event.FuncEventFree.c_func(self._ptr)
            self._ptr = None

    @property
    def type(self):
        """Event's Type
        :rtype: EventType
        """
        return self._type

    @property
    def tid(self):
        """Event's transaction ID
        :rtype: int
        """
        return self._tid

    @property
    def did(self):
        """Event's dialog ID
        :rtype: int
        """
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
