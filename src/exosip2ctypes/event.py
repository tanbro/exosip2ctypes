# -*- coding: utf-8 -*-

"""
eXosip2 event API

see: http://www.antisip.com/doc/exosip2/group__eXosip2__event.html
"""

from ctypes import string_at, byref
from enum import IntEnum

from ._c import event
from .utils import b2s
from .message import OsipMessage

__all__ = ['Event', 'EventType']


class Event:
    def __init__(self, ptr):
        """Class for event description

        :param ptr: Pointer to `struct eXosip_event_t`
        """
        self._ptr = ptr
        self._type = EventType(int(ptr.contents.type))
        self._textinfo = b2s(ptr.contents.textinfo)
        self._request = OsipMessage(ptr.contents.request)
        self._response = OsipMessage(ptr.contents.response)
        self._ack = OsipMessage(ptr.contents.ack)
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

    def __str__(self):
        try:
            cls_name = self.__class__.__qualname__
        except AttributeError:
            cls_name = '.'.join([__name__, self.__class__.__name__])
        return '<%s type:%s textinfo:%s tid:%s did:%s rid:%s cid:%s sid:%s nid:%s>' % (
            cls_name, self._type, self._textinfo, self._tid, self._did, self._rid, self._cid, self._sid, self._nid
        )

    def dispose(self):
        """Free resource in an eXosip event.

        .. attention::

            Cause `eXosip` do not manage the `struct eXosip_event_t *` automatic, we shall free it manually!
            The memory free action is done in :class:`Event` 's destruction.
            so you can either ``del`` the event object or use the ``with`` statement,
            python's GC will free memory when the object is destructed.
        """
        if self._ptr:
            event.FuncEventFree.c_func(self._ptr)
            self._ptr = None
            self._request = None
            self._response = None
            self._ack = None

    @property
    def type(self):
        """type of the event

        :rtype: EventType
        """
        return self._type

    @property
    def textinfo(self):
        """text description of event

        :rtype: str
        """
        return self._textinfo

    @property
    def request(self):
        """request within current transaction

        :rtype: OsipMessage
        """
        return self._request

    @property
    def response(self):
        """last response within current transaction

        :rtype: OsipMessage
        """
        return self._response

    @property
    def ack(self):
        """ack within current transaction

        :rtype: OsipMessage
        """
        return self._ack

    @property
    def tid(self):
        """unique id for transactions (to be used for answers)

        :rtype: int
        """
        return self._tid

    @property
    def did(self):
        """unique id for SIP dialogs

        :rtype: int
        """
        return self._did

    @property
    def rid(self):
        """unique id for registration

        :rtype: int
        """
        return self._rid

    @property
    def cid(self):
        """unique id for SIP calls (but multiple dialogs!)

        :rtype: int
        """
        return self._cid

    @property
    def sid(self):
        """unique id for outgoing subscriptions

        :rtype: int
        """
        return self._sid

    @property
    def nid(self):
        """unique id for incoming subscriptions

        :rtype: int
        """
        return self._nid

    @property
    def ss_status(self):
        """current Subscription-State for subscription

        :rtype: int
        """
        return self._ss_status

    @property
    def ss_reason(self):
        """current Reason status for subscription

        :rtype: int
        """
        return self._ss_reason

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()


class EventType(IntEnum):
    """Enumeration of event types
    """

    #: user is successfully registred.
    registration_success = event.EXOSIP_REGISTRATION_SUCCESS
    #: user is not registred.
    registration_failure = event.EXOSIP_REGISTRATION_FAILURE
    #: announce a new call
    call_invite = event.EXOSIP_CALL_INVITE
    #: announce a new INVITE within call
    call_reinvite = event.EXOSIP_CALL_REINVITE
    #: announce no answer within the timeout
    call_noanswer = event.EXOSIP_CALL_NOANSWER
    #: announce processing by a remote app
    call_proceeding = event.EXOSIP_CALL_PROCEEDING
    #: announce ringback
    call_ringing = event.EXOSIP_CALL_RINGING
    #: announce start of call
    call_answered = event.EXOSIP_CALL_ANSWERED
    #: announce a redirection
    call_redirected = event.EXOSIP_CALL_REDIRECTED
    #: announce a request failure
    call_requestfailure = event.EXOSIP_CALL_REQUESTFAILURE
    #: announce a server failure
    call_serverfailure = event.EXOSIP_CALL_SERVERFAILURE
    #: announce a global failure
    call_globalfailure = event.EXOSIP_CALL_GLOBALFAILURE
    #: ACK received for 200ok to INVITE
    call_ack = event.EXOSIP_CALL_ACK
    #: announce that call has been cancelled
    call_cancelled = event.EXOSIP_CALL_CANCELLED
    #: announce new incoming request.
    call_message_new = event.EXOSIP_CALL_MESSAGE_NEW
    #: announce a 1xx for request.
    call_message_proceeding = event.EXOSIP_CALL_MESSAGE_PROCEEDING
    #: announce a 200ok
    call_message_answered = event.EXOSIP_CALL_MESSAGE_ANSWERED
    #: announce a redirection.
    call_message_redirected = event.EXOSIP_CALL_MESSAGE_REDIRECTED
    #: announce a failure.
    call_message_requestfailure = event.EXOSIP_CALL_MESSAGE_REQUESTFAILURE
    #: announce a failure.
    call_message_serverfailure = event.EXOSIP_CALL_MESSAGE_SERVERFAILURE
    #: announce a failure.
    call_message_globalfailure = event.EXOSIP_CALL_MESSAGE_GLOBALFAILURE
    #: a BYE was received for this call
    call_closed = event.EXOSIP_CALL_CLOSED
    #: call context is cleared.
    call_released = event.EXOSIP_CALL_RELEASED
    #: announce new incoming request.
    message_new = event.EXOSIP_MESSAGE_NEW
    #: announce a 1xx for request.
    message_proceeding = event.EXOSIP_MESSAGE_PROCEEDING
    #: announce a 200ok
    message_answered = event.EXOSIP_MESSAGE_ANSWERED
    #: announce a redirection.
    message_redirected = event.EXOSIP_MESSAGE_REDIRECTED
    #: announce a failure.
    message_requestfailure = event.EXOSIP_MESSAGE_REQUESTFAILURE
    #: announce a failure.
    message_serverfailure = event.EXOSIP_MESSAGE_SERVERFAILURE
    #: announce a failure.
    message_globalfailure = event.EXOSIP_MESSAGE_GLOBALFAILURE
    #: announce no answer
    subscription_noanswer = event.EXOSIP_SUBSCRIPTION_NOANSWER
    #: announce a 1xx
    subscription_proceeding = event.EXOSIP_SUBSCRIPTION_PROCEEDING
    #: announce a 200ok
    subscription_answered = event.EXOSIP_SUBSCRIPTION_ANSWERED
    #: announce a redirection
    subscription_redirected = event.EXOSIP_SUBSCRIPTION_REDIRECTED
    #: announce a request failure
    subscription_requestfailure = event.EXOSIP_SUBSCRIPTION_REQUESTFAILURE
    #: announce a server failure
    subscription_serverfailure = event.EXOSIP_SUBSCRIPTION_SERVERFAILURE
    #: announce a global failure
    subscription_globalfailure = event.EXOSIP_SUBSCRIPTION_GLOBALFAILURE
    #: announce new NOTIFY request
    subscription_notify = event.EXOSIP_SUBSCRIPTION_NOTIFY
    #: announce new incoming SUBSCRIBE.
    in_subscription_new = event.EXOSIP_IN_SUBSCRIPTION_NEW
    #: announce no answer
    notification_noanswer = event.EXOSIP_NOTIFICATION_NOANSWER
    #: announce a 1xx
    notification_proceeding = event.EXOSIP_NOTIFICATION_PROCEEDING
    #: announce a 200ok
    notification_answered = event.EXOSIP_NOTIFICATION_ANSWERED
    #: announce a redirection
    notification_redirected = event.EXOSIP_NOTIFICATION_REDIRECTED
    #: announce a request failure
    notification_requestfailure = event.EXOSIP_NOTIFICATION_REQUESTFAILURE
    #: announce a server failure
    notification_serverfailure = event.EXOSIP_NOTIFICATION_SERVERFAILURE
    #: announce a global failure
    notification_globalfailure = event.EXOSIP_NOTIFICATION_GLOBALFAILURE
    #: MAX number of events
    event_count = event.EXOSIP_EVENT_COUNT
