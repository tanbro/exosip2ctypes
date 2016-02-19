# -*- coding: utf-8 -*-

"""
eXosip2 event API

see: http://www.antisip.com/doc/exosip2/group__eXosip2__event.html
"""

from ctypes import POINTER, Structure, c_uint, c_int, c_void_p, c_char

from . import globs
from .utils import ExosipFunc

EXOSIP_REGISTRATION_SUCCESS = 0
EXOSIP_REGISTRATION_FAILURE = 1
EXOSIP_CALL_INVITE = 2
EXOSIP_CALL_REINVITE = 3
EXOSIP_CALL_NOANSWER = 4
EXOSIP_CALL_PROCEEDING = 5
EXOSIP_CALL_RINGING = 6
EXOSIP_CALL_ANSWERED = 7
EXOSIP_CALL_REDIRECTED = 8
EXOSIP_CALL_REQUESTFAILURE = 9
EXOSIP_CALL_SERVERFAILURE = 10
EXOSIP_CALL_GLOBALFAILURE = 11
EXOSIP_CALL_ACK = 12
EXOSIP_CALL_CANCELLED = 13
EXOSIP_CALL_MESSAGE_NEW = 14
EXOSIP_CALL_MESSAGE_PROCEEDING = 15
EXOSIP_CALL_MESSAGE_ANSWERED = 16
EXOSIP_CALL_MESSAGE_REDIRECTED = 17
EXOSIP_CALL_MESSAGE_REQUESTFAILURE = 18
EXOSIP_CALL_MESSAGE_SERVERFAILURE = 19
EXOSIP_CALL_MESSAGE_GLOBALFAILURE = 20
EXOSIP_CALL_CLOSED = 21
EXOSIP_CALL_RELEASED = 22
EXOSIP_MESSAGE_NEW = 23
EXOSIP_MESSAGE_PROCEEDING = 24
EXOSIP_MESSAGE_ANSWERED = 25
EXOSIP_MESSAGE_REDIRECTED = 26
EXOSIP_MESSAGE_REQUESTFAILURE = 27
EXOSIP_MESSAGE_SERVERFAILURE = 28
EXOSIP_MESSAGE_GLOBALFAILURE = 29
EXOSIP_SUBSCRIPTION_NOANSWER = 30
EXOSIP_SUBSCRIPTION_PROCEEDING = 31
EXOSIP_SUBSCRIPTION_ANSWERED = 32
EXOSIP_SUBSCRIPTION_REDIRECTED = 33
EXOSIP_SUBSCRIPTION_REQUESTFAILURE = 34
EXOSIP_SUBSCRIPTION_SERVERFAILURE = 35
EXOSIP_SUBSCRIPTION_GLOBALFAILURE = 36
EXOSIP_SUBSCRIPTION_NOTIFY = 37
EXOSIP_IN_SUBSCRIPTION_NEW = 38
EXOSIP_NOTIFICATION_NOANSWER = 39
EXOSIP_NOTIFICATION_PROCEEDING = 40
EXOSIP_NOTIFICATION_ANSWERED = 41
EXOSIP_NOTIFICATION_REDIRECTED = 42
EXOSIP_NOTIFICATION_REQUESTFAILURE = 43
EXOSIP_NOTIFICATION_SERVERFAILURE = 44
EXOSIP_NOTIFICATION_GLOBALFAILURE = 45
EXOSIP_EVENT_COUNT = 46


class Event(Structure):
    """
    Structure for event description
    """
    _fields_ = [
        ('type', c_uint),  #: type of the event
        ('textinfo', c_char * 256),  #: text description of event
        ('external_reference', c_void_p),  #: external reference (for calls)
        ('request', c_void_p),  #: request within current transaction
        ('response', c_void_p),  #: last response within current transaction
        ('ack', c_void_p),  #: ack within current transaction
        ('tid', c_int),  #: unique id for transactions (to be used for answers)
        ('did', c_int),  #: unique id for transactions (to be used for answers)
        ('rid', c_int),  #: unique id for registration
        ('cid', c_int),  #: unique id for SIP calls (but multiple dialogs!)
        ('sid', c_int),  #: unique id for outgoing subscriptions
        ('nid', c_int),  #: unique id for incoming subscriptions
        ('ss_status', c_int),  #: unique id for incoming subscriptions
        ('ss_reason', c_int),  #: current Reason status for subscription
    ]


class FuncEventWait(ExosipFunc):
    func_name = 'event_wait'
    argtypes = [c_void_p, c_int, c_int]
    restype = POINTER(Event)


class FuncEventFree(ExosipFunc):
    func_name = 'event_free'
    argtypes = [c_void_p]


globs.func_classes.extend([
    FuncEventWait,
    FuncEventFree,
])
