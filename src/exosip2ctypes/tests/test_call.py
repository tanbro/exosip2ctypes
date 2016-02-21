import sys
import unittest
from unittest.mock import Mock
from threading import Condition
import logging
import logging.config

from exosip2ctypes import initialize, unload, call, Context, EventType

logging.basicConfig(
    level=logging.DEBUG, stream=sys.stdout,
    format='%(asctime)-15s [%(threadName)-10s] [%(levelname)-7s] %(name)s - %(message)s'
)


class SingleCallTest(unittest.TestCase):
    ADDR1 = ('127.0.0.1', 50060)
    ADDR2 = ('127.0.0.1', 51060)

    @classmethod
    def setUpClass(cls):
        initialize()

    @classmethod
    def tearDownClass(cls):
        unload()

    def setUp(self):
        self.ctx1 = Context()
        self.ctx2 = Context()
        self.ctx1.listen_on_address(address=self.ADDR1[0], port=self.ADDR1[1])
        self.ctx2.listen_on_address(address=self.ADDR2[0], port=self.ADDR2[1])
        self.ctx1.start()
        self.ctx2.start()

    def tearDown(self):
        self.ctx1.stop()
        self.ctx2.stop()

    def test_call_self(self):
        m = Mock()
        cond = Condition()
        recv_call_id = None

        def event_cb(_, evt):
            if evt.type == EventType.call_invite:
                m()
                nonlocal recv_call_id
                recv_call_id = evt.request.call_id
                cond.acquire()
                cond.notify()
                cond.release()

        self.ctx1.event_callback = event_cb
        # start call
        cond.acquire()
        # build and send invitation message
        with self.ctx1.lock:
            msg = call.InitInvite(
                self.ctx1,
                to='sip:{0[0]}:{0[1]}'.format(self.ADDR1),
                from_='sip:{0[0]}:{0[1]}'.format(self.ADDR1),
            )
            send_call_id = msg.call_id
            self.ctx1.call_send_init_invite(msg)
        # wait event result!
        cond.wait()
        cond.release()
        # assertion
        self.assertEqual(m.call_count, 1)
        self.assertEqual(recv_call_id, send_call_id)


if __name__ == '__main__':
    unittest.main()
