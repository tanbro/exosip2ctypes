import sys
import logging
import logging.config

from exosip2ctypes import initialize, Context, register, EventType

logging.basicConfig(
    level=logging.DEBUG, stream=sys.stdout,
    format='%(asctime)-15s [%(threadName)-10s] [%(levelname)-7s] %(name)s - %(message)s'
)


def on_sip_event(context, evt):
    if evt.type == EventType.registration_success:
        logging.info('registration success: %s', evt)

    elif evt.type == EventType.registration_failure:
        logging.error('registration failure: %s', evt)

    elif evt.type == EventType.message_new:
        logging.debug('%s', evt.request)


initialize()
ctx = Context(event_callback=on_sip_event)

logging.debug('listening...')
ctx.listen_on_address(port=55160)
logging.debug('starting...')

ctx.start()
logging.debug('started!')

with ctx.lock:
    ctx.add_authentication_info('user', 'auth-user', 'password', None)

while True:
    s = sys.stdin.readline().strip().lower()
    if s in ('q', 'quit'):
        ctx.stop()
        break
    elif s == 'r':
        with ctx.lock:
            register_req = register.InitialRegister(
                ctx,
                'sip:user@host:port',
                'sip:proxy:port'
            )
            logging.debug('rid=%s', register_req.rid)
            logging.debug('InitialRegister=%s', register_req)
            register_req.send()
