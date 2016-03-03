import unittest
import sys
import threading
import random
import logging
from time import time, sleep

from exosip2ctypes import initialize, unload, Context

logging.basicConfig(
    level=logging.DEBUG, stream=sys.stdout,
    format='%(asctime)-15s [%(threadName)-10s] [%(levelname)-7s] %(name)s - %(message)s'
)


class ContextTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initialize()

    @classmethod
    def tearDownClass(cls):
        unload()

    def setUp(self):
        self.ctx = Context()

    def tearDown(self):
        self.ctx.quit()
        self.ctx = None

    def test_lock(self):
        self.assertFalse(self.ctx.lock.locked())

        self._flag = 0

        def r1():
            sleep(random.random())
            self.ctx.lock_acquire()
            self.assertTrue(self.ctx.lock.locked())
            self._flag = 1
            sleep(random.random())
            self.assertEqual(self._flag, 1)
            self.ctx.lock_release()

        def r2():
            sleep(random.random())
            with self.ctx.lock:
                self.assertTrue(self.ctx.lock.locked())
                self._flag = 2
                sleep(random.random())
                self.assertEqual(self._flag, 2)

        def r3():
            sleep(random.random())
            self.ctx.lock.acquire()
            self.assertTrue(self.ctx.lock.locked())
            self._flag = 3
            sleep(random.random())
            self.assertEqual(self._flag, 3)
            self.ctx.lock.release()

        t1 = threading.Thread(target=r1)
        t2 = threading.Thread(target=r2)
        t3 = threading.Thread(target=r3)
        thread_list = [t1, t2, t3]
        random.shuffle(thread_list)
        for ti in thread_list:
            ti.start()
        random.shuffle(thread_list)
        for ti in thread_list:
            ti.join()
        #
        self.assertFalse(self.ctx.lock.locked())

    def test_listen(self):
        self.ctx.listen_on_address()

    def test_ua(self):
        ua = self.ctx.user_agent
        self.assertTrue(ua)
        new_val = 'this is a create user_agent'
        self.ctx.user_agent = new_val
        self.assertEqual(self.ctx.user_agent, new_val)

    def test_event_wait_one_second(self):
        start = int(time())
        event = self.ctx.event_wait(1, 0)
        self.assertGreaterEqual(int(time()), start)
        self.assertIsNone(event)

    def test_start_and_stop(self):
        self.ctx.start()
        self.assertTrue(self.ctx.is_running)
        self.ctx.stop()
        self.assertFalse(self.ctx.is_running)


if __name__ == '__main__':
    unittest.main()
