# -*- coding: utf-8 -*-

"""eXosip call API

This file provide the API needed to control calls. You can use it to:

    * build initial invite.
    * send initial invite.
    * build request within the call.
    * send request within the call.

This API can be used to build the following messages:
   INVITE, INFO, OPTIONS, REFER, UPDATE, NOTIFY
"""

from ctypes import byref, create_string_buffer, c_void_p, c_int

from ._c import call
from .error import raise_if_osip_error
from .message import ExosipMessage
from .utils import s2b

__all__ = ['InitInvite', 'Ack', 'Answer']


class InitInvite(ExosipMessage):
    def __init__(self, context, to, from_, route=None, subject=None):
        """Build a default INVITE message for a new call.

        :param Context context: :class:`Context` object contains the `eXosip_t` instance.
        :param str to: SIP url for callee.
        :param str from_: SIP url for caller.
        :param str route: Route header for INVITE. (optional)
        :param str subject: Subject for the call.
        """
        ptr = c_void_p()  # osip_message_t* invite = NULL;
        pc_to = create_string_buffer(s2b(to))
        pc_from = create_string_buffer(s2b(from_))
        pc_route = create_string_buffer(s2b(route)) if route else None
        pc_subject = create_string_buffer(s2b(subject)) if subject else None
        error_code = call.FuncCallBuildInitialInvite.c_func(
            context.ptr, byref(ptr), pc_to, pc_from, pc_route, pc_subject
        )
        raise_if_osip_error(error_code)
        self._to = to
        self._from = from_
        self._route = route
        self._subject = subject
        super(InitInvite, self).__init__(ptr, context)

    @property
    def to(self):
        """SIP url for callee.

        :rtype: str
        """
        return self.to

    @property
    def from_(self):
        """SIP url for caller.

        :rtype: str
        """
        return self._from

    @property
    def route(self):
        """Route header for INVITE. (optional)

        :rtype: str
        """
        return self._route

    @property
    def subject(self):
        """Subject for the call.

        :rtype: str
        """
        return self._subject


class Ack(ExosipMessage):
    def __init__(self, context, did):
        """Build a default ACK for a 200ok received.

        :param Context context: eXosip instance.
        :param int did: dialog id of call.
        """
        ptr = c_void_p()  # struct osip_message_t *p = NULL;
        err_code = call.FuncCallBuildAck.c_func(context.ptr, c_int(did), byref(ptr))
        raise_if_osip_error(err_code)
        super(Ack, self).__init__(ptr, context)
        self._did = did

    @property
    def did(self):
        """
        :return: dialog id of call.
        :rtype: int
        """
        return self._did


class Answer(ExosipMessage):
    def __init__(self, context, tid, status):
        """Build default Answer for request.

        :param Context context: eXosip instance.
        :param int tid: id of transaction to answer.
        :param int status: Status code to use.
        """
        ptr = c_void_p()  # struct osip_message_t *p = NULL;
        err_code = call.FuncCallBuildAnswer.c_func(context.ptr, c_int(tid), c_int(status), byref(ptr))
        raise_if_osip_error(err_code)
        super(Answer, self).__init__(ptr, context)
        self._tid = tid
        self._status = status

    @property
    def tid(self):
        """
        :return: id of transaction to answer.
        :rtype: int
        """
        return self._tid

    @property
    def status(self):
        """
        :return: Status code to use.
        :rtype: int
        """
        return self._status
