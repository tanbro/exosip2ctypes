# -*- coding: utf-8 -*-

"""
eXosip2 event API

see: http://www.antisip.com/doc/exosip2/group__eXosip2__event.html
"""

from enum import IntEnum

from ._c import event
from .utils import to_str
from .message import ExosipMessage

__all__ = ['Event', 'EventType']


class Event:
    def __init__(self, ptr, context):
        """Class for event description

        :param ctypes.c_void_p ptr: `struct eXosip_event_t *ptr`
        :param Context context: eXosip context
        """
        if not ptr:
            raise RuntimeError('Null pointer.')
        if not context:
            raise RuntimeError('No context.')
        self._ptr = ptr
        self._context = context
        self._type = EventType(ptr.contents.type)
        self._textinfo = to_str(ptr.contents.textinfo)
        self._request = ExosipMessage(ptr.contents.request, context) if ptr.contents.request else None
        self._response = ExosipMessage(ptr.contents.response, context) if ptr.contents.response else None
        self._ack = ExosipMessage(ptr.contents.ack, context) if ptr.contents.ack else None
        self._tid = ptr.contents.tid
        self._did = ptr.contents.did
        self._rid = ptr.contents.rid
        self._cid = ptr.contents.cid
        self._sid = ptr.contents.sid
        self._nid = ptr.contents.nid
        self._ss_status = ptr.contents.ss_status
        self._ss_reason = ptr.contents.ss_reason

    def __del__(self):
        self.dispose()

    def __str__(self):
        try:
            cls_name = '{0.__module__:s}.{0.__qualname__:s}'.format(self.__class__)
        except AttributeError:
            cls_name = '{0.__module__:s}.{0.__name__:s}'.format(self.__class__)
        return '<{} instance at 0x{:x}, type:{} textinfo:{!r} tid:{} did:{} rid:{} cid:{} sid:{} nid:{}>'.format(
            cls_name, id(self),
            self._type.name, self._textinfo, self._tid, self._did, self._rid, self._cid, self._sid, self._nid
        )

    def dispose(self):
        """Free resource in an eXosip event.

        .. danger::
            After called this method, `struct eXosip_event_t` of the object is freed,
            following attributes will be `None`:

                * :attr:`request`
                * :attr:`response`
                * :attr:`ack`

            It is invoked in class destructor.
            Don't call it yourself, let Python runtime's GC dispose the structure.
        """
        if self._ptr:
            event.FuncEventFree.c_func(self._ptr)
            self._ptr = None
            self._request = None
            self._response = None
            self._ack = None

    @property
    def disposed(self):
        """Is resource in an eXosip event disposed

        :rtype: bool
        """
        return self._ptr is None

    @property
    def type(self):
        """type of the event

        :rtype: EventType
        """
        return self._type

    @property
    def textinfo(self):
        """
        :return: text description of event
        :rtype: str
        """
        return self._textinfo

    @property
    def request(self):
        """
        :return: request within current transaction
        :rtype: ExosipMessage
        """
        if not self._ptr:
            raise RuntimeError('OsipMessage structure has been disposed.')
        return self._request

    @property
    def response(self):
        """
        :return: last response within current transaction
        :rtype: ExosipMessage
        """
        if not self._ptr:
            raise RuntimeError('OsipMessage structure has been disposed.')
        return self._response

    @property
    def ack(self):
        """
        :return: ack within current transaction
        :rtype: OsipMessage
        """
        if not self._ptr:
            raise RuntimeError('OsipMessage structure has been disposed.')
        return self._ack

    @property
    def tid(self):
        """
        :return: unique id for transactions (to be used for answers)
        :rtype: int
        """
        return self._tid

    @property
    def did(self):
        """
        :return: unique id for SIP dialogs
        :rtype: int
        """
        return self._did

    @property
    def rid(self):
        """
        :return: unique id for registration
        :rtype: int
        """
        return self._rid

    @property
    def cid(self):
        """
        :return: unique id for SIP calls (but multiple dialogs!)
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
        """
        :return: unique id for incoming subscriptions
        :rtype: int
        """
        return self._nid

    @property
    def ss_status(self):
        """
        :return: current Subscription-State for subscription
        :rtype: int
        """
        return self._ss_status

    @property
    def ss_reason(self):
        """
        :return: current Reason status for subscription
        :rtype: int
        """
        return self._ss_reason


class EventType(IntEnum):
    """Enumeration of event types
    """

    #: user is successfully registred.
    registration_success = event.EXOSIP_REGISTRATION_SUCCESS
    #: user is not registred.
    registration_failure = event.EXOSIP_REGISTRATION_FAILURE
    #: announce a create call
    call_invite = event.EXOSIP_CALL_INVITE
    #: announce a create INVITE within call
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
    #: announce create incoming request.
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
    #: announce create incoming request.
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
    #: announce create NOTIFY request
    subscription_notify = event.EXOSIP_SUBSCRIPTION_NOTIFY
    #: announce create incoming SUBSCRIBE.
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
    # #: MAX number of events
    # event_count = event.EXOSIP_EVENT_COUNT
