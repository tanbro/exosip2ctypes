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
from .event import Event
from .utils import b2s, s2b, LoggerMixin
from .version import get_library_version

__all__ = ['Context', 'ContextEventHandler', 'ContextLock']


class BaseContext:
    pass


class Context(BaseContext, LoggerMixin):
    def __init__(self, event_handler=None, contact_address=(None, 0)):
        """Allocate and Initiate an eXosip context.

        :param ContextEventHandler event_handler: An object gathers all event callbacks for the context
        :param contact_address: address used in `Contact` header. See :meth:`masquerade_contact`
        :type contact_address: tuple<ip_address: str, port: int>
        """
        self.logger.info('<0x%x>__init__: contact_address=%s', id(self), contact_address)
        self._ptr = conf.FuncMalloc.c_func()
        self.logger.debug('<0x%x>__init__: eXosip_malloc() -> %s', id(self), self._ptr)
        if self._ptr is None:
            raise MallocError()
        error_code = conf.FuncInit.c_func(self._ptr)
        raise_if_osip_error(error_code)
        self._locked = False
        self._lock = ContextLock(self)
        if contact_address[0]:
            self.masquerade_contact(*contact_address)
        self._user_agent = '{} ({} ({}/{}))'.format(DLL_NAME, get_library_version(), platform.machine(),
                                                    platform.system())
        self._set_user_agent(self._user_agent)
        self._is_running = False
        self._stop_sentinel = False
        self._loop_thread = None
        self._start_cond = threading.Condition()
        self._stop_cond = threading.Condition()
        self._event_handler = event_handler

    def __del__(self):
        self.logger.info('<0x%x>__del__', id(self))
        if self._is_running:
            self.stop()
        if self._ptr:
            self.quit()

    def _loop(self, s, ms):
        """Context main loop.

        :param s: seconds for :meth:`event_wait`
        :param ms: milliseconds for :meth:`event_wait`

        It's running in a separated thread, and won't return util :meth:`stop` called or set :attr:`started` to `False`
        """
        self.logger.debug('<0x%x>_loop: >>>', id(self))
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
                    self.logger.debug('<0x%x>_loop: event_wait() -> %s', id(self), evt)
                    with evt:
                        self.process_event(evt)
        finally:
            self._stop_cond.acquire()
            self._is_running = False
            self._stop_sentinel = False
            self._stop_cond.notify()
            self._stop_cond.release()
        self.logger.debug('<0x%x>_loop: <<<', id(self))

    def _set_user_agent(self, user_agent):
        conf.FuncSetUserAgent.c_func(self._ptr, c_char_p(s2b(user_agent)))

    @property
    def ptr(self):
        """C Pointer to the context's `eXosip_t` C structure
        """
        return self._ptr

    @property
    def event_handler(self):
        """Event handler for the context

        :rtype: ContextEventHandler
        """
        return self._event_handler

    @event_handler.setter
    def event_handler(self, val):
        self._event_handler = val

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

        * Setting to `True` equals to call :meth:`start()`
        * Setting to `False` equals to call :meth:`stop()`
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
        if self._ptr:
            self.logger.debug('<0x%x>quit: eXosip_quit(%s)', id(self), self._ptr)
            conf.FuncQuit.c_func(self._ptr)
            self._ptr = None
        self.logger.info('<0x%x>quit: <<<', id(self))

    def masquerade_contact(self, public_address, port):
        """This method is used to replace contact address with the public address of your NAT.
        The ip address should be retrieved manually (fixed IP address) or with STUN.
        This address will only be used when the remote correspondent appears to be on an DIFFERENT LAN.

        If set to `None`, then the local ip address will be guessed automatically (returns to default mode).

        :param str public_address: the ip address.
        :param int port: the port for masquerading.
        """
        self.logger.info('<0x%x>masquerade_contact: public_address=%s, port=%s', id(self), public_address, port)
        conf.FuncMasqueradeContact.c_func(
            self._ptr,
            create_string_buffer(s2b(public_address)) if public_address else None,
            c_int(port) if public_address else 0
        )

    def listen_on_address(self, address=None, transport=socket.IPPROTO_UDP, port=5060, family=socket.AF_INET,
                          secure=False):
        """Listen on a specified socket.

        :param str address: the address to bind (`NULL` for all interface)
        :param int transport: `IPPROTO_UDP` for udp. (soon to come: TCP/TLS?)
        :param int port: the listening port. (0 for random port)
        :param int family: the IP family (AF_INET or AF_INET6).
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
        :return: event or `None` if no event
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

        Equal to set :attr:`is_running` to `True`
        """
        self.logger.info('<0x%x>start: >>> s=%s, ms=%s', id(self), s, ms)
        if self._is_running:
            raise RuntimeError("Context loop already started.")
        self._loop_thread = threading.Thread(target=self._loop, args=(s, ms))
        self._start_cond.acquire()
        self._loop_thread.start()
        self._start_cond.wait()
        self._start_cond.release()
        self.logger.info('<0x%x>start: <<< -> %s', id(self), self._loop_thread)
        return self._loop_thread

    def stop(self):
        """Stop the context's main loop thread and return after the thread stopped.

        Equal to set :attr:`is_running` to `False`
        """
        self.logger.info('<0x%x>stop: >>>', id(self))
        if not self._is_running:
            raise RuntimeError("Context loop not started.")
        self._stop_cond.acquire()
        self._stop_sentinel = True
        self._stop_cond.wait()
        self._stop_cond.release()
        self.logger.info('<0x%x>stop: <<<', id(self))

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
        self.logger.info('<0x%x>run: >>> s=%s, ms=%s, timeout=%s', id(self), s, ms, timeout)
        self.start(s, ms)
        self._loop_thread.join(timeout)
        self.logger.info('<0x%x>run: <<<', id(self))

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
        callback_name = 'on_{}'.format(evt.type.name)
        if isinstance(self._event_handler, dict):
            callback = self._event_handler.get(callback_name, None)
        else:
            callback = getattr(self._event_handler, callback_name, None)
        if callable(callback):
            self.logger.debug('<0x%x>process_event: %s: callback >>>', id(self), evt)
            callback(self, evt)
            self.logger.debug('<0x%x>process_event: %s: callback <<<', id(self), evt)


class ContextEventHandler:
    """A class where defines event callbacks for a context

    You can inherit it or write your own handler class, and define event handler callback methods in the your class::

        class MyEventHandler(ContextEventHandler):
            def on_call_invite(self, ctx, evt):
                # do sth...
                pass

            def on_xxxx(self, ctx, evt):
                # do sth...
                pass

        ctx.event_handler = MyEventHandler()

    Or just assign callable objects to the instance's on_xxx attributes::

        def my_on_call_invite(ctx, evt):
            # do sth...
            pass

        ctx.event_handler = ContextEventHandler()
        ctx.event_handler.on_call_invite = my_on_call_invite

    Event handler callback methods names format are: ``on_<event_type>``, eg:

      * ``on_call_invite``
      * ``on_call_answered``
      * ``on_call_closed``
      * ``on_xxx``

    In which, the ``<event_type>`` part is :class:`exosip2ctypes.event.EventType` enumeration member item name.

    Every event handler callback method has two parameters:

        1. :class:`Context` ``ctx`` - eXosip context on which event triggered.
        2. :class:`exosip2ctypes.event.Event` ``evt`` - triggered event.

    See :class:`exosip2ctypes.event.EventType` for event types definitions.

    .. tip::
        Any `dict` has `on_<event_type>` key or `object` has `on_<event_type>` attributes,
        and the attributes/items are callable who has two parameters an be assigned to the :attr:`Context.event_handler`

    .. warning::
        Events are fired in the context's main loop thread,
        so the event handler function should return as soon as possible to avoid blocking the main loop.
    """
    pass


class ContextLock:
    def __init__(self, context):
        """A helper class for eXosip Context lock

        :param Context context: Context which the lock is for

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
