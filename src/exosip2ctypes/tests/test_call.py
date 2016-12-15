import sys
import unittest
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock
from threading import Condition
import logging
import logging.config

from exosip2ctypes import initialize, unload, call, Context, EventType

logging.basicConfig(
    level=logging.DEBUG, stream=sys.stdout,
    format='%(asctime)-15s [%(threadName)-10s] [%(levelname)-7s] %(name)s - %(message)s'
)


class SingleCallTest(unittest.TestCase):
    listen_address = ('127.0.0.1', 50060)

    @classmethod
    def setUpClass(cls):
        initialize()

    @classmethod
    def tearDownClass(cls):
        unload()

    def setUp(self):
        self.ctx = Context()
        self.ctx.listen_on_address(address=self.listen_address[0], port=self.listen_address[1])
        self.ctx.start()

    def tearDown(self):
        self.ctx.stop()

    def test_call_self(self):
        m = Mock()
        cond = Condition()
        self._recv_call_id = None

        def event_cb(_, evt):
            if evt.type == EventType.call_invite:
                m()
                self._recv_call_id = evt.request.call_id
            # condition of event callback returning
            cond.acquire()
            cond.notify()
            cond.release()

        self.ctx.event_callback = event_cb
        # start call:
        # build and send invitation message
        cond.acquire()
        with self.ctx.lock:
            msg = call.InitInvite(
                self.ctx,
                to_url='sip:{0[0]}:{0[1]}'.format(self.listen_address),
                from_url='sip:{0[0]}:{0[1]}'.format(self.listen_address),
            )
            send_call_id = msg.call_id
            self.ctx.call_send_init_invite(msg)
        # wait event result!
        cond.wait(1)
        cond.release()
        # assertion
        self.assertEqual(m.call_count, 1)
        self.assertEqual(self._recv_call_id, send_call_id)


if __name__ == '__main__':
    unittest.main()
