import unittest

from time import time

from .. import load, Context


class ContextTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load()

    def setUp(self):
        self.ctx = Context()

    def tearDown(self):
        self.ctx.quit()
        self.ctx = None

    def test_lock(self):
        self.ctx.lock()
        self.ctx.unlock()

    def test_listen(self):
        self.ctx.listen_on_address()

    def test_ua(self):
        ua = self.ctx.user_agent
        self.assertTrue(ua)
        new_val = 'this is a new user_agent'
        self.ctx.user_agent = new_val
        self.assertEqual(self.ctx.user_agent, new_val)

    def test_event_wait_one_second(self):
        start = int(time())
        event = self.ctx.event_wait(1, 0)
        self.assertGreaterEqual(int(time()), start)
        self.assertIsNone(event)

if __name__ == '__main__':
    unittest.main()
