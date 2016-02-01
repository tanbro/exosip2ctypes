# -*- coding: utf-8 -*-

"""
eXosip2 context API
"""

from ctypes import c_char_p, c_int
import platform
import socket
import threading

from ._c import DLL_NAME, conf, event, auth
from .error import MallocError, ExitNotZeroError
from .event import Event, EventType
from .version import get_library_version


__all__ = ['Context']


class ContextLock:
    def __init__(self, context):
        self._context = context

    def acquire(self):
        self._context.lock()

    def release(self):
        self._context.unlock

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class Context:
    def __init__(self):
        self._p = conf.FuncMalloc.c_func()
        if self._p is None:
            raise MallocError()
        ret = conf.FuncInit.c_func(self._p)
        if ret != 0:
            raise ExitNotZeroError(conf.FuncInit.func_name, ret)
        self._user_agent = '{} ({} ({}/{}))'.format(DLL_NAME, get_library_version(), platform.machine(),
                                                    platform.system())
        self._set_user_agent(self._user_agent)
        self._context_lock = ContextLock(self)
        self._started = False
        self._stop_sentinel = False
        self._loop_thread = None
        self._start_cond = threading.Condition()
        self._stop_cond = threading.Condition()

    def _loop(self, s, ms):
        self._start_cond.acquire
        self._started = True
        self._start_cond.notify()
        self._start_cond.release
        try:
            while not self._stop_sentinel:
                with self.event_wait(s, ms) as evt:
                    with self._context_lock:
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
        conf.FuncSetUserAgent.c_func(
            self._p,
            c_char_p(user_agent.encode())
        )

    @property
    def pointer(self):
        return self._p

    @property
    def context_lock(self):
        return self._context_lock

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
        return self._user_agent

    @user_agent.setter
    def user_agent(self, val):
        self._set_user_agent(val)
        self._user_agent = val

    def quit(self):
        conf.FuncQuit.c_func(self._p)
        self._p = None

    def lock(self):
        conf.FuncLock.c_func(self._p)

    def unlock(self):
        conf.FuncUnlock.c_func(self._p)

    def listen_addr(self, addr='localhost', transport=socket.IPPROTO_UDP, port=5060,
                    family=socket.AF_INET, secure=False):
        if transport not in [socket.IPPROTO_TCP, socket.IPPROTO_UDP]:
            raise RuntimeError('Unsupported socket transport type %s' % transport)
        if family not in [socket.AF_INET, socket.AF_INET6]:
            raise RuntimeError('Unsupported socket family typo %s' % family)
        ret = conf.FuncListenAddr.c_func(
            self._p,
            c_int(transport),
            c_char_p(addr.encode()),
            c_int(port),
            c_int(family),
            c_int(secure)
        )
        ret = int(ret)
        if ret != 0:
            raise ExitNotZeroError(conf.FuncListenAddr.func_name, ret)

    def event_wait(self, s, ms):
        ret = event.FuncEventWait.c_func(self._p, c_int(s), c_int(ms))
        if ret:
            return Event(ret)
        else:
            return None

    def automatic_action(self):
        auth.FuncAutomaticAction.c_func(self._p)

    def start(self, s=0, ms=50):
        self._loop_thread = threading.Thread(target=self._loop, args=(s, ms))
        self._start_cond.acquire()
        self._loop_thread.start()
        self._start_cond.wait()
        self._start_cond.release()

    def stop(self):
        if not self._started:
            return
        self._stop_cond.acquire()
        self._stop_sentinel = True
        self._stop_cond.wait()
        self._stop_cond.release()

    def run(self, s=0, ms=50, timeout=None):
        self.start(s, ms)
        self._loop_thread.join(timeout)

    def process_event(self, evt):
        if evt.type == EventType.CALL_INVITE:
            self.on_call_invite(evt)

    def on_call_invite(self, evt):
        pass
