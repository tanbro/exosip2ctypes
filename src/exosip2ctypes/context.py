# -*- coding: utf-8 -*-

"""
eXosip2 context API
"""

import platform
import socket
import threading
from ctypes import c_char_p, c_int, create_string_buffer

from ._c import DLL_NAME, conf, event, auth, call
from .error import MallocError, raise_if_osip_error
from .event import Event, EventType
from .utils import b2s, s2b
from .version import get_library_version

__all__ = ['Context', 'ContextLock']


class ContextLock:
    """eXosip Context lock's python class
    """

    def __init__(self, context):
        """
        :param Context context: Context which the lock is for
        """
        self._context = context

    def acquire(self):
        self._context.internal_lock()

    def release(self):
        self._context.internal_unlock()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class Context:
    def __init__(self, contact_address=(None, 0), using_internal_lock=False):
        """Allocate and Initiate an eXosip context.

        :param contact_address: address used in `Contact` header. See :meth:`masquerade_contact`
        :type contact_address: tuple<ip_address: str, port: int>
        :param bool using_internal_lock: Is the :attr:`lock` using Python stdlib's :class:`threading.Lock` or eXosip2's context lock. Default `False` (using Python's)
        """
        self._ptr = conf.FuncMalloc.c_func()
        if self._ptr is None:
            raise MallocError()
        err_code = conf.FuncInit.c_func(self._ptr)
        raise_if_osip_error(err_code)
        if contact_address[0]:
            self.masquerade_contact(*contact_address)
        self._user_agent = '{} ({} ({}/{}))'.format(DLL_NAME, get_library_version(), platform.machine(),
                                                    platform.system())
        self._set_user_agent(self._user_agent)
        if using_internal_lock:
            self._lock = ContextLock(self)
        else:
            self._lock = threading.Lock()
        self._started = False
        self._stop_sentinel = False
        self._loop_thread = None
        self._start_cond = threading.Condition()
        self._stop_cond = threading.Condition()

    def _loop(self, s, ms):
        """Context main loop

        It won't return util :meth:`stop` called or set :attr:`started` to `False`
        :param s: seconds for :meth:`event_wait`
        :param ms: milliseconds for :meth:`event_wait`
        """
        self._start_cond.acquire()
        self._started = True
        self._start_cond.notify()
        self._start_cond.release()
        try:
            while not self._stop_sentinel:
                evt = self.event_wait(s, ms)
                if evt is None:
                    continue
                with evt:
                    with self._lock:
                        self.automatic_action()
                    if evt:
                        self.process_event(evt)
        finally:
            self._stop_cond.acquire()
            self._started = False
            self._stop_sentinel = False
            self._stop_cond.notify()
            self._stop_cond.release()

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
        :rtype: threading.Lock or ContextLock
        """
        return self._lock

    @property
    def started(self):
        """
        :return: Is the context's main loop started
        """
        return self._started

    @started.setter
    def started(self, val):
        """
        :param bool val: start or stop the context's main loop
        """
        if val:
            self.start()
        else:
            self.stop()

    @property
    def user_agent(self):
        """
        :return: Context's user agent string
        :rtype: str
        """
        return b2s(self._user_agent)

    @user_agent.setter
    def user_agent(self, val):
        """
        :param str val: Context's user agent string
        """
        self._set_user_agent(val)
        self._user_agent = val

    def internal_lock(self):
        """Lock the eXtented oSIP library.
        """
        conf.FuncLock.c_func(self._ptr)

    def internal_unlock(self):
        """UnLock the eXtented oSIP library.
        """
        conf.FuncUnlock.c_func(self._ptr)

    def quit(self):
        """Release ressource used by the eXtented oSIP library.
        """
        conf.FuncQuit.c_func(self._ptr)
        self._ptr = None

    def masquerade_contact(self, public_address, port):
        """This method is used to replace contact address with the public address of your NAT. The ip address should be retreived manually (fixed IP address) or with STUN. This address will only be used when the remote correspondant appears to be on an DIFFERENT LAN.

        If set to `None`, then the local ip address will be guessed automatically (returns to default mode).

        :param str public_address: the ip address.
        :param int port: the port for masquerading.
        """
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
        if transport not in [socket.IPPROTO_TCP, socket.IPPROTO_UDP]:
            raise RuntimeError('Unsupported socket transport type %s' % transport)
        if family not in [socket.AF_INET, socket.AF_INET6]:
            raise RuntimeError('Unsupported socket family type %s' % family)
        err_code = conf.FuncListenAddr.c_func(
            self._ptr,
            c_int(transport),
            c_char_p(s2b(address)),
            c_int(port),
            c_int(family),
            c_int(secure)
        )
        raise_if_osip_error(err_code)

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
        if self._started:
            raise RuntimeError("Context loop already started.")
        self._loop_thread = threading.Thread(target=self._loop, args=(s, ms))
        self._start_cond.acquire()
        self._loop_thread.start()
        self._start_cond.wait()
        self._start_cond.release()

    def stop(self):
        if not self._started:
            raise RuntimeError("Context loop not started.")
        self._stop_cond.acquire()
        self._stop_sentinel = True
        self._stop_cond.wait()
        self._stop_cond.release()

    def run(self, s=0, ms=50, timeout=None):
        self.start(s, ms)
        self._loop_thread.join(timeout)

    # def send_message(self, message):
    #     if isinstance(message, call.Message):
    #         self.call_send_answer(message=message)
    #     else:
    #         raise TypeError('Unsupported libeXosip2 message type %s' % type(message))

    def call_terminate(self, cid, did):
        err_code = call.FuncCallTerminate.c_func(self._ptr, int(cid), int(did))
        raise_if_osip_error(err_code)

    def call_send_ack(self, did=None, message=None):
        if message is not None:
            did = message.did
        err_code = call.FuncCallSendAck.c_func(
            self._ptr,
            c_int(did),
            message.ptr if message else None
        )
        raise_if_osip_error(err_code)

    def call_send_answer(self, tid=None, status=None, message=None):
        if message is not None:
            tid = message.tid
            status = message.status
        err_code = call.FuncCallSendAnswer.c_func(
            self._ptr,
            c_int(tid),
            c_int(status),
            message.ptr if message else None
        )
        raise_if_osip_error(err_code)

    def process_event(self, evt):
        if evt.type == EventType.call_invite:
            self.on_call_invite(evt)
        elif evt.type == EventType.call_cancelled:
            self.on_call_cancelled(evt)
        elif evt.type == EventType.call_answered:
            self.on_call_answered(evt)
        elif evt.type == EventType.call_closed:
            self.on_call_closed(evt)

    def on_call_invite(self, evt):
        pass

    def on_call_cancelled(self, evt):
        pass

    def on_call_answered(self, evt):
        pass

    def on_call_closed(self, evt):
        pass
