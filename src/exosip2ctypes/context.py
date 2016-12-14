# -*- coding: utf-8 -*-

"""
eXosip2 context API
"""

import sys
import platform
import socket
import threading
from ctypes import c_char_p, c_int, create_string_buffer
from concurrent.futures import ThreadPoolExecutor

from ._c import conf, event, authentication, call
from ._c.lib import DLL_NAME
from .error import MallocError, raise_if_osip_error
from .event import Event
from .utils import to_str, to_bytes, LoggerMixin
from .version import get_library_version

__all__ = ['Context', 'ContextLock']

_IS_PY2 = sys.version_info[0] < 3


class BaseContext:
    pass


class Context(BaseContext, LoggerMixin):
    def __init__(self, event_callback=None):
        """Allocate and Initiate an eXosip context.

        :param callable event_callback: Event callback.

            It's a callback function or any other callable object.
            You can avoid the parameter in constructor, and set :attr:`event_callback` later.

            The callback is like::

                def event_callback(context, event):
                    # do some thing...
                    pass

            It has two parameters:
                * :class:`Context` : eXosip context on which the event happened.
                * :class:`Event` : The event happened.
        """
        self.logger.info('<0x%x>__init__', id(self))
        self._ptr = conf.FuncMalloc.c_func()
        self.logger.debug('<0x%x>__init__: eXosip_malloc() -> %s', id(self), self._ptr)
        if self._ptr is None:
            raise MallocError()
        error_code = conf.FuncInit.c_func(self._ptr)
        raise_if_osip_error(error_code)
        self._event_callback = None
        self.set_event_callback(event_callback)
        self._event_executor = None
        self._locked = False
        self._lock = ContextLock(self)
        self._user_agent = '{} ({} ({}/{}))'.format(DLL_NAME, get_library_version(), platform.machine(),
                                                    platform.system())
        self._set_user_agent(self._user_agent)
        self._is_running = False
        self._stop_sentinel = False
        self._event_loop_thread = None
        self._start_cond = threading.Condition()
        self._stop_cond = threading.Condition()

    def __del__(self):
        self.logger.info('<0x%x>__del__', id(self))
        self.quit()

    def _event_loop(self, s, ms):
        """Context main loop.

        :param s: seconds for :meth:`event_wait`
        :param ms: milliseconds for :meth:`event_wait`

        It's running in a separated thread, and won't return util :meth:`stop` called or set :attr:`started` to `False`
        """
        self.logger.debug('<0x%x>_event_loop: >>>', id(self))
        self._start_cond.acquire()
        self._is_running = True
        self._start_cond.notify()
        self._start_cond.release()
        try:
            while not self._stop_sentinel:
                self.lock_acquire()
                try:
                    self.automatic_action()
                finally:
                    self.lock_release()
                evt = self.event_wait(s, ms)
                if evt:
                    self.logger.debug('<0x%x>_event_loop: event_wait() -> %s', id(self), evt)
                    if callable(self._event_callback):
                        def execute_event(_evt):
                            def done(f):
                                self.logger.debug('<0x%x>_event_loop: event<0x%x> callback <<<', id(self), id(_evt))
                                exc = f.exception()
                                if exc:
                                    try:
                                        raise exc
                                    except:
                                        self.logger.exception('')
                                        raise

                            self._event_executor.submit(self._event_callback, self, evt).add_done_callback(done)

                        self.logger.debug('<0x%x>_event_loop: event<0x%x> callback >>>', id(self), id(evt))
                        execute_event(evt)
        finally:
            self._stop_cond.acquire()
            self._is_running = False
            self._stop_sentinel = False
            self._stop_cond.notify()
            self._stop_cond.release()
        self.logger.debug('<0x%x>_loop: <<<', id(self))

    def _set_user_agent(self, user_agent):
        pch = create_string_buffer(to_bytes(user_agent))
        conf.FuncSetUserAgent.c_func(self._ptr, pch)

    @property
    def ptr(self):
        """C Pointer to the context's `eXosip_t` C structure

        :rtype: ctypes.c_void_p
        """
        return self._ptr

    def get_event_callback(self):
        """Set event callback

        :rtype: callable

        .. attention:: Event callback is invoked in a :class:`concurrent.futures.Executor`
        """
        return self._event_callback

    def set_event_callback(self, val):
        """Set event callback

        :param callable val: callback function

        .. attention:: Event callback is invoked in a :class:`concurrent.futures.Executor`
        """
        if val is not None:
            if not callable(val):
                raise TypeError('"event_callback" is not callable')
        self._event_callback = val

    event_callback = property(get_event_callback, set_event_callback)

    @property
    def lock(self):
        """eXosip Context lock.

        :rtype: :class:`ContextLock`
        """
        return self._lock

    @property
    def locked(self):
        """True if the context has been acquired by some thread, False if not.

        :rtype: bool
        """
        return self._locked

    @property
    def is_running(self):
        """Is the context's main loop running

        :rtype: bool

        * It will be `True` after calling :meth:`start` or :meth:`run`
        * It will be `False` after calling :meth:`stop`
        """
        return self._is_running

    @property
    def user_agent(self):
        """Context's user agent string

        :rtype: str
        """
        return to_str(self._user_agent)

    @user_agent.setter
    def user_agent(self, val):
        self._set_user_agent(val)
        self._user_agent = val

    def lock_acquire(self):
        """Lock the eXtented oSIP library.
        """
        conf.FuncLock.c_func(self._ptr)
        self._locked = True

    def lock_release(self):
        """UnLock the eXtented oSIP library.
        """
        self._locked = False
        conf.FuncUnlock.c_func(self._ptr)

    def quit(self):
        """Release resource used by the eXtented oSIP library.
        """
        self.logger.info('<0x%x>quit: >>>', id(self))
        if self._is_running:
            self.stop()
        if self._ptr:
            self.logger.debug('<0x%x>quit: eXosip_quit(%s)', id(self), self._ptr)
            conf.FuncQuit.c_func(self._ptr)
            self._ptr = None
        self.logger.info('<0x%x>quit: <<<', id(self))

    def masquerade_contact(self, public_address=None, port=0):
        """This method is used to replace contact address with the public address of your NAT.
        The ip address should be retrieved manually (fixed IP address) or with STUN.
        This address will only be used when the remote correspondent appears to be on an DIFFERENT LAN.

        If set to `None`, then the local ip address will be guessed automatically (returns to default mode).

        :param str public_address: the ip address.
        :param int port: the port for masquerading.

        .. note:: It's advised to call the method after :meth:`listen_on_address`
        """
        self.logger.info('<0x%x>masquerade_contact: public_address=%s, port=%s', id(self), public_address, port)
        conf.FuncMasqueradeContact.c_func(
            self._ptr,
            create_string_buffer(to_bytes(public_address)) if public_address else None,
            c_int(port) if public_address else 0
        )

    def listen_on_address(self, address=None, transport=socket.IPPROTO_UDP, port=5060, family=socket.AF_INET,
                          secure=False):
        """Listen on a specified socket.

        :param str address: the address to bind (`NULL` for all interface)
        :param int transport: :data:`socket.IPPROTO_UDP` for udp. (soon to come: TCP/TLS?)
        :param int port: the listening port. (0 for random port)
        :param int family: the IP family (:data:`socket.AF_INET` or :data:`socket.AF_INET6`).
        :param bool secure: `False` for UDP or TCP, `True` for TLS (with TCP).
        """
        self.logger.info(
            '<0x%x>listen_on_address: '
            'address=%s, transport=%s, port=%s, family=%s, secure=%s',
            id(self), address, transport, port, family, secure
        )
        if transport not in [socket.IPPROTO_TCP, socket.IPPROTO_UDP]:
            raise RuntimeError('Unsupported socket transport type {}'.format(transport))
        if family not in [socket.AF_INET, socket.AF_INET6]:
            raise RuntimeError('Unsupported socket family type {}'.format(family))
        error_code = conf.FuncListenAddr.c_func(
            self._ptr,
            c_int(transport),
            c_char_p(to_bytes(address)),
            c_int(port),
            c_int(family),
            c_int(secure)
        )
        raise_if_osip_error(error_code)

    def event_wait(self, s, ms):
        """Wait for an eXosip event.

        :param int s: timeout value (seconds).
        :param int ms: timeout value (seconds).
        :return: event or `None` if no event
        :rtype: Event
        """
        evt_ptr = event.FuncEventWait.c_func(self._ptr, c_int(s), c_int(ms))
        if evt_ptr:
            return Event(evt_ptr, self)
        else:
            return None

    def automatic_action(self):
        """Initiate some automatic actions:

        * Retry with credentials upon reception of 401/407.
        * Retry with higher Sessions-Expires upon reception of 422.
        * Refresh REGISTER and SUBSCRIBE before the expiration delay.
        * Retry with Contact header upon reception of 3xx request.
        * Send automatic UPDATE for session-timer feature.
        """
        authentication.FuncAutomaticAction.c_func(self._ptr)

    def start(self, s=0, ms=50, event_executor=None):
        """Start the main loop for the context in a create thread, and then return.

        :param int s: timeout value (seconds). Passed to :meth:`event_wait` in the main loop.
        :param int ms: timeout value (seconds). Passed to :meth:`event_wait` in the main loop.
        :param concurrent.futures.Executor event_executor: Event executor instance. Events will be fired in it.
            Default is a :class:`concurrent.futures.ThreadPoolExecutor` instance
        :return: New created event loop thread.
        :rtype: threading.Thread

        This method returns soon after the main loop thread started, so it **does not block**.

        Equal to set :attr:`is_running` to `True`
        """
        self.logger.info('<0x%x>start: >>> s=%s, ms=%s', id(self), s, ms)
        if self._is_running:
            raise RuntimeError("Context loop already started.")
        self._event_executor = event_executor or ThreadPoolExecutor()
        self._event_loop_thread = threading.Thread(target=self._event_loop, args=(s, ms))
        self._start_cond.acquire()
        self._event_loop_thread.start()
        self._start_cond.wait()
        self._start_cond.release()
        self.logger.info('<0x%x>start: <<< -> %s', id(self), self._event_loop_thread)
        return self._event_loop_thread

    def stop(self):
        """Stop the context's main loop thread and return after the thread stopped.

        Equal to set :attr:`is_running` to `False`
        """
        self.logger.info('<0x%x>stop: >>>', id(self))
        if not self._is_running:
            raise RuntimeError("Context loop not started.")
        self.logger.info('<0x%x>stop: terminate event loop', id(self))
        self._stop_cond.acquire()
        self._stop_sentinel = True
        self._stop_cond.wait()
        self._stop_cond.release()
        self.logger.info('<0x%x>stop: shutdown event executor', id(self))
        self._event_executor.shutdown()
        self.logger.info('<0x%x>stop: <<<', id(self))

    def run(self, s=0, ms=50, event_executor=None, timeout=None):
        """Start the main loop for the context in a create thread, and then wait until the thread terminates.

        :param int s: timeout value (seconds). Passed to :meth:`event_wait` in the main loop.
        :param int ms: timeout value (seconds). Passed to :meth:`event_wait` in the main loop.
        :param concurrent.futures.Executor event_executor: see the same parameter in :meth:`start`.
        :param float timeout: When the timeout argument is present and not None, it should be a floating point number
                              specifying a timeout for the operation in seconds (or fractions thereof)

        This method **blocks**, it equals::

            trd = context.start(s, ms)
            trd.join(timeout)
        """
        self.logger.info('<0x%x>run: >>> s=%s, ms=%s, timeout=%s', id(self), s, ms, timeout)
        self.start(s, ms, event_executor)
        self._event_loop_thread.join(timeout)
        self.logger.info('<0x%x>run: <<<', id(self))

    def build_message(self, message_class, *args, **kwargs):
        """Build a default message for a eXosip transaction/dialog/call

        :param type(ExosipMessage) message_class: Message Class
        :param args: Sequent arguments passed to the class constructor
        :param kwargs: Named arguments passed to the class constructor
        :return: New built message object
        :rtype: ExosipMessage
        """
        return message_class(self, *args, **kwargs)

    # def send_message(self, message):
    #     if isinstance(message, call.Message):
    #         self.call_send_answer(message=message)
    #     else:
    #         raise TypeError('Unsupported libeXosip2 message type %s' % type(message))

    def call_terminate(self, cid, did=0):
        """Terminate a call. send CANCEL, BYE or 603 Decline.

        :param int cid: call id of call.
        :param int did: dialog id of call.
        """
        error_code = call.FuncCallTerminate.c_func(self._ptr, c_int(cid), c_int(did))
        raise_if_osip_error(error_code)

    def call_send_init_invite(self, invite):
        """Initiate a call.

        :param call.InitInvite invite: SIP INVITE message to send.
        :return: CID - unique id for SIP calls (but multiple dialogs!)
        :rtype: int

        .. attention:: returned `call id` is an integer, which different from SIP message's `Call-Id` header
        """
        result = call.FuncCallSendInitialInvite.c_func(self._ptr, invite.ptr)
        raise_if_osip_error(result)
        return int(result)

    def call_send_ack(self, did=None, ack=None):
        """Send the ACK for the 200ok received.

        :param int did: dialog id of call.
        :param call.Ack ack: SIP ACK message to send. `did` won't be used if specified.
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
        :param call.Answer answer: The sip answer to send. `tid` and `status` won't be used if specified.
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

    def add_authentication_info(self, user_name, user_id, password, realm):
        """Add authentication credentials.

        :param str user_name: username
        :param str user_id: login (usually equals the username)
        :param str password: password
        :param str realm: realm within which credentials apply, or `None` to apply credentials to unrecognized realms

        These are used when an outgoing request comes back with an authorization required response.
        """
        error_code = authentication.FuncAddAuthenticationInfo.c_func(
            self._ptr,
            create_string_buffer(to_bytes(user_name)) if user_name else None,
            create_string_buffer(to_bytes(user_id)) if user_id else None,
            create_string_buffer(to_bytes(password)) if password else None,
            None,
            create_string_buffer(to_bytes(realm)) if realm else None
        )
        raise_if_osip_error(error_code)

    def remove_authentication_info(self, user_name, realm):
        """Remove authentication credentials.

        :param str user_name: user name
        :param str realm: realm must be exact same arg as for :meth:`add_authentication_info`
        """
        error_code = authentication.FuncRemoveAuthenticationInfo.c_func(
            self._ptr,
            create_string_buffer(to_bytes(user_name)) if user_name else None,
            create_string_buffer(to_bytes(realm)) if realm else None
        )
        raise_if_osip_error(error_code)


class ContextLock:
    """A helper class for eXosip Context lock

    This class wraps eXosip's native context lock function,
    which is invoked in :meth:`Context.lock_acquire` and :meth:`Context.lock_release`.
    You can call theses methods directly, or use :attr:`Context.lock`.

    ``with`` statement is supported.

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

    .. danger:: Do **NOT** construct the class yourself, use :attr:`Context.lock`.
    """

    def __init__(self, context):
        """
        :param Context context: Context which the lock is for
        """
        self._context = context

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self):
        """lock the context"""
        self._context.lock_acquire()

    def release(self):
        """unlock the context"""
        self._context.lock_release()

    def locked(self):
        """Return the status of the lock: True if it has been acquired by some thread, False if not.

        :rtype: bool
        """
        return self._context.locked
