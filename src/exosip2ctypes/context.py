# -*- coding: utf-8 -*-

"""
eXosip2 context API
"""

import platform
import socket
import threading
from ctypes import c_char_p, c_int

from ._c import DLL_NAME, conf, event, auth, call
from .error import MallocError, raise_if_osip_error
from .event import Event, EventType
from .utils import b2s, s2b
from .version import get_library_version

__all__ = ['Context', 'ContextLock']


class ContextLock:
    def __init__(self, context):
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
    def __init__(self, using_internal_lock=False):
        self._ptr = conf.FuncMalloc.c_func()
        if self._ptr is None:
            raise MallocError()
        err_code = conf.FuncInit.c_func(self._ptr)
        raise_if_osip_error(err_code)
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
        return self._ptr

    @property
    def lock(self):
        return self._lock

    @property
    def started(self):
        return self._started

    @started.setter
    def started(self, val):
        if val:
            self.start()
        else:
            self.stop()

    @property
    def user_agent(self):
        return b2s(self._user_agent)

    @user_agent.setter
    def user_agent(self, val):
        self._set_user_agent(val)
        self._user_agent = val

    def internal_lock(self):
        conf.FuncLock.c_func(self._ptr)

    def internal_unlock(self):
        conf.FuncUnlock.c_func(self._ptr)

    def quit(self):
        conf.FuncQuit.c_func(self._ptr)
        self._ptr = None

    def listen_on_address(self, address='localhost', transport=socket.IPPROTO_UDP, port=5060, family=socket.AF_INET,
                          secure=False):
        if transport not in [socket.IPPROTO_TCP, socket.IPPROTO_UDP]:
            raise RuntimeError('Unsupported socket transport type %s' % transport)
        if family not in [socket.AF_INET, socket.AF_INET6]:
            raise RuntimeError('Unsupported socket family typo %s' % family)
        err_code = conf.FuncListenAddr.c_func(
            self._ptr,
            c_int(transport),
            c_char_p(address.encode()),
            c_int(port),
            c_int(family),
            c_int(secure)
        )
        raise_if_osip_error(err_code)

    def event_wait(self, s, ms):
        evt_ptr = event.FuncEventWait.c_func(self._ptr, c_int(s), c_int(ms))
        if evt_ptr:
            return Event(evt_ptr)
        else:
            return None

    def automatic_action(self):
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

    def on_call_invite(self, evt):
        pass

