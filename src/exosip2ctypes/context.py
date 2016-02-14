# -*- coding: utf-8 -*-

"""
eXosip2 context API
"""

import platform
import socket
import threading
from ctypes import c_char_p, c_int, create_string_buffer

from ._c import conf, event, auth, call
from ._c.lib import DLL_NAME
from .error import MallocError, raise_if_osip_error
from .event import Event, EventType
from .utils import b2s, s2b, LogMixin
from .version import get_library_version

__all__ = ['Context', 'ContextLock']


class Context(LogMixin):
    def __init__(self, contact_address=(None, 0), using_internal_lock=False):
        """Allocate and Initiate an eXosip context.

        :param contact_address: address used in `Contact` header. See :meth:`masquerade_contact`
        :type contact_address: tuple<ip_address: str, port: int>
        :param bool using_internal_lock:
            Is the :attr:`lock` using Python stdlib's :class:`threading.Lock` or eXosip2's native context lock.
            Default `False` (using Python's)
        """
        self.logger.info('<%s>__init__: contact_address=%s, using_internal_lock=%s',
                         hex(id(self)), contact_address, using_internal_lock)
        self._ptr = conf.FuncMalloc.c_func()
        self.logger.debug('<%s>__init__: malloc() -> %s', hex(id(self)), self._ptr)
        if self._ptr is None:
            raise MallocError()
        error_code = conf.FuncInit.c_func(self._ptr)
        raise_if_osip_error(error_code)
        if contact_address[0]:
            self.masquerade_contact(*contact_address)
        self._user_agent = '{} ({} ({}/{}))'.format(DLL_NAME, get_library_version(), platform.machine(),
                                                    platform.system())
        self._set_user_agent(self._user_agent)
        if using_internal_lock:
            self._lock = ContextLock(self)
        else:
            self._lock = threading.Lock()
        self._is_running = False
        self._stop_sentinel = False
        self._loop_thread = None
        self._start_cond = threading.Condition()
        self._stop_cond = threading.Condition()

    def __del__(self):
        self.logger.info('<%s>__del__', hex(id(self)))
        if self._is_running:
            self.stop()
        self.quit()

    def _loop(self, s, ms):
        """Context main loop

        It won't return util :meth:`stop` called or set :attr:`started` to `False`
        :param s: seconds for :meth:`event_wait`
        :param ms: milliseconds for :meth:`event_wait`
        """
        self.logger.debug('<%s>_loop: >>>', hex(id(self)))
        self._start_cond.acquire()
        self._is_running = True
        self._start_cond.notify()
        self._start_cond.release()
        try:
            while not self._stop_sentinel:
                with self._lock:
                    self.automatic_action()
                evt = self.event_wait(s, ms)
                if evt:
                    with evt:
                        self.process_event(evt)
        finally:
            self._stop_cond.acquire()
            self._is_running = False
            self._stop_sentinel = False
            self._stop_cond.notify()
            self._stop_cond.release()
        self.logger.debug('<%s>_loop: <<<', hex(id(self)))

    def _set_user_agent(self, user_agent):
        conf.FuncSetUserAgent.c_func(self._ptr, c_char_p(s2b(user_agent)))

    @property
    def ptr(self):
        """C Pointer to the context's `eXosip_t` C structure
        """
        return self._ptr

    @property
    def lock(self):
        """eXosip Context lock.

        :return: Python stdlib's `threading.Lock` if `using_internal_lock` is `False`, else eXosip's native lock.
        :type: :class:`ContextLock` or :class:`threading.Lock`
        """
        return self._lock

    @property
    def is_running(self):
        """Whether the context's main loop started or not

        :rtype: bool

        * Set it to `True` equals :meth:`start()`
        * Set it to `False` equals :meth:`stop()`
        """
        return self._is_running

    @is_running.setter
    def is_running(self, val):
        if val:
            self.start()
        else:
            self.stop()

    @property
    def user_agent(self):
        """Context's user agent string

        :rtype: str
        """
        return b2s(self._user_agent)

    @user_agent.setter
    def user_agent(self, val):
        self._set_user_agent(val)
        self._user_agent = val

    def internal_lock(self):
        """Lock the eXtented oSIP library, using eXosip's native lock.
        """
        conf.FuncLock.c_func(self._ptr)

    def internal_unlock(self):
        """UnLock the eXtented oSIP library, using eXosip's native lock.
        """
        conf.FuncUnlock.c_func(self._ptr)

    def quit(self):
        """Release resource used by the eXtented oSIP library.
        """
        self.logger.info('<%s>quit: >>>', hex(id(self)))
        if self._ptr:
            self.logger.debug('<%s>quit: quit(%s)', hex(id(self)), self._ptr)
            conf.FuncQuit.c_func(self._ptr)
            self._ptr = None
        self.logger.info('<%s>quit: <<<', hex(id(self)))

    def masquerade_contact(self, public_address, port):
        """This method is used to replace contact address with the public address of your NAT. The ip address should be retreived manually (fixed IP address) or with STUN. This address will only be used when the remote correspondant appears to be on an DIFFERENT LAN.

        If set to `None`, then the local ip address will be guessed automatically (returns to default mode).

        :param str public_address: the ip address.
        :param int port: the port for masquerading.
        """
        self.logger.info('<%s>masquerade_contact: public_address=%s, port=%s', hex(id(self)), public_address, port)
        conf.FuncMasqueradeContact.c_func(
            self._ptr,
            create_string_buffer(s2b(public_address)) if public_address else None,
            c_int(port) if public_address else 0
        )

    def listen_on_address(self, address=None, transport=socket.IPPROTO_UDP, port=5060, family=socket.AF_INET,
                          secure=False):
        """Listen on a specified socket.

        :param address: the address to bind (`NULL` for all interface)
        :param transport: `IPPROTO_UDP` for udp. (soon to come: TCP/TLS?)
        :param port: the listening port. (0 for random port)
        :param family: the address to bind (NULL for all interface)
        :param secure: `False` for UDP or TCP, `True` for TLS (with TCP).
        """
        self.logger.info(
            '<%s>listen_on_address: '
            'address=%s, transport=%s, port=%s, family=%s, secure=%s',
            hex(id(self)), address, transport, port, family, secure
        )
        if transport not in [socket.IPPROTO_TCP, socket.IPPROTO_UDP]:
            raise RuntimeError('Unsupported socket transport type %s' % transport)
        if family not in [socket.AF_INET, socket.AF_INET6]:
            raise RuntimeError('Unsupported socket family type %s' % family)
        error_code = conf.FuncListenAddr.c_func(
            self._ptr,
            c_int(transport),
            c_char_p(s2b(address)),
            c_int(port),
            c_int(family),
            c_int(secure)
        )
        raise_if_osip_error(error_code)

    def event_wait(self, s, ms):
        """Wait for an eXosip event.

        :param int s: timeout value (seconds).
        :param int ms: timeout value (seconds).
        :return: event triggered, `None` if nothing happened
        :rtype: Event
        """
        evt_ptr = event.FuncEventWait.c_func(self._ptr, c_int(s), c_int(ms))
        if evt_ptr:
            return Event(evt_ptr)
        else:
            return None

    def automatic_action(self):
        """Initiate some automatic actions:

            * Retry with credentials upon reception of 401/407.
            * Retry with higher Session-Expires upon reception of 422.
            * Refresh REGISTER and SUBSCRIBE before the expiration delay.
            * Retry with Contact header upon reception of 3xx request.
            * Send automatic UPDATE for session-timer feature.
        """
        auth.FuncAutomaticAction.c_func(self._ptr)

    def start(self, s=0, ms=50):
        """Start the main loop for the context in a new thread, and then return.

        :param int s: timeout value (seconds). Passed to :meth:`event_wait` in the main loop.
        :param int ms: timeout value (seconds). Passed to :meth:`event_wait` in the main loop.
        :return: New created thread.
        :rtype: threading.Thread

        This method returns soon after the main loop thread started, so it **does not block**.

        Invoke the method equals set :attr:`is_running` to `True`
        """
        self.logger.info('<%s>start: >>> s=%s, ms=%s', hex(id(self)), s, ms)
        if self._is_running:
            raise RuntimeError("Context loop already started.")
        self._loop_thread = threading.Thread(target=self._loop, args=(s, ms))
        self._start_cond.acquire()
        self._loop_thread.start()
        self._start_cond.wait()
        self._start_cond.release()
        self.logger.info('<%s>start: <<<', hex(id(self)))
        return self._loop_thread

    def stop(self):
        """Stop the main loop for the context

        Returns after the main loop thread stopped.

        Invoke the method equals set :attr:`is_running` to `False`
        """
        self.logger.info('<%s>stop: >>>', hex(id(self)))
        if not self._is_running:
            raise RuntimeError("Context loop not started.")
        self._stop_cond.acquire()
        self._stop_sentinel = True
        self._stop_cond.wait()
        self._stop_cond.release()
        self.logger.info('<%s>stop: <<<', hex(id(self)))

    def run(self, s=0, ms=50, timeout=None):
        """Start the main loop for the context in a new thread, and then wait until the thread terminates.

        :param int s: timeout value (seconds). Passed to :meth:`event_wait` in the main loop.
        :param int ms: timeout value (seconds). Passed to :meth:`event_wait` in the main loop.
        :param float timeout: When the timeout argument is present and not None, it should be a floating point number
                              specifying a timeout for the operation in seconds (or fractions thereof)

        This method **blocks**, it equals::

            trd = context.start(s, ms)
            trd.join(timeout)
        """
        self.logger.info('<%s>run: >>> s=%s, ms=%s, timeout=%s', hex(id(self)), s, ms, timeout)
        self.start(s, ms)
        self._loop_thread.join(timeout)
        self.logger.info('<%s>run: <<<', hex(id(self)))

    # def send_message(self, message):
    #     if isinstance(message, call.Message):
    #         self.call_send_answer(message=message)
    #     else:
    #         raise TypeError('Unsupported libeXosip2 message type %s' % type(message))

    def call_terminate(self, cid, did):
        """Terminate a call. send CANCEL, BYE or 603 Decline.

        :param int cid: call id of call.
        :param int did: dialog id of call.
        """
        error_code = call.FuncCallTerminate.c_func(self._ptr, int(cid), int(did))
        raise_if_osip_error(error_code)

    def call_send_init_invite(self, invite):
        """Initiate a call.

        :param call.InitInvite invite: SIP INVITE message to send.
        :return: unique id for SIP calls (but multiple dialogs!)
        :rtype: int

        .. attention:: returned `call id` is an integer, which different from SIP message's `Call-Id` header
        """
        result = call.FuncCallSendInitialInvite.c_func(self._ptr, invite.ptr)
        raise_if_osip_error(result)
        return int(result)

    def call_send_ack(self, did=None, ack=None):
        """Send the ACK for the 200ok received.

        :param int did: dialog id of call.
        :param call.Ack ack: SIP ACK message to send.
        """
        if ack is not None:
            did = ack.did
        error_code = call.FuncCallSendAck.c_func(
            self._ptr,
            c_int(did),
            ack.ptr if ack else None
        )
        raise_if_osip_error(error_code)

    def call_send_answer(self, tid=None, status=None, answer=None):
        """Send Answer for invite.

        :param int tid: id of transaction to answer.
        :param int status: response status if `answer` is NULL. (not allowed for 2XX)
        :param call.Answer answer: The sip answer to send.
        """
        if answer is not None:
            tid = answer.tid
            status = answer.status
        error_code = call.FuncCallSendAnswer.c_func(
            self._ptr,
            c_int(tid),
            c_int(status),
            answer.ptr if answer else None
        )
        raise_if_osip_error(error_code)

    def process_event(self, evt):
        """Process the events generated in the main loop, and then trigger event callbacks.

        :param Event evt: Event generated in the main loop
        """
        self.logger.debug('<%s>process_event: >>> %s', hex(id(self)), evt)
        if evt.type == EventType.call_invite:
            self.on_call_invite(evt)
        elif evt.type == EventType.call_cancelled:
            self.on_call_cancelled(evt)
        elif evt.type == EventType.call_answered:
            self.on_call_answered(evt)
        elif evt.type == EventType.call_closed:
            self.on_call_closed(evt)
        elif evt.type == EventType.call_ack:
            self.on_call_ack(evt)
        elif evt.type == EventType.call_ringing:
            self.on_call_ringing(evt)
        elif evt.type == EventType.call_requestfailure:
            self.on_call_requestfailure(evt)
        elif evt.type == EventType.call_noanswer:
            self.on_call_noanswer(evt)
        elif evt.type == EventType.call_proceeding:
            self.on_call_proceeding(evt)
        elif evt.type == EventType.call_serverfailure:
            self.on_call_serverfailure(evt)
        elif evt.type == EventType.call_released:
            self.on_call_released(evt)
        self.logger.debug('<%s>process_event: <<<', hex(id(self)))

    def on_call_invite(self, evt):
        pass

    def on_call_cancelled(self, evt):
        pass

    def on_call_answered(self, evt):
        pass

    def on_call_closed(self, evt):
        pass

    def on_call_ack(self, evt):
        pass

    def on_call_ringing(self, evt):
        pass

    def on_call_requestfailure(self, evt):
        pass

    def on_call_noanswer(self, evt):
        pass

    def on_call_proceeding(self, evt):
        pass

    def on_call_serverfailure(self, evt):
        pass

    def on_call_released(self, evt):
        pass


class ContextLock:
    def __init__(self, context):
        """eXosip Context lock's python class

        :param Context context: Context which the lock is for

        | This class wraps eXosip's native context lock.
        | Use :meth:`acquire` to lock and :meth:`release` to unlock.
        | ``with`` statement is supported.

        eg::

            context.lock.acquire()
            try:
                do_something()
                # ...
            finally:
                context.lock.release()

        or::

            with context.lock:
                do_something()
                # ...

        """
        self._context = context

    def acquire(self):
        """lock"""
        self._context.internal_lock()

    def release(self):
        """unlock"""
        self._context.internal_unlock()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
