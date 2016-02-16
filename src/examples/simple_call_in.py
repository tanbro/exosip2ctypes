import sys
import logging.config

from exosip2ctypes import initialize, Context, call

logging.basicConfig(
    level=logging.DEBUG, stream=sys.stdout,
    format='%(asctime)-15s [%(threadName)-10s] [%(levelname)-7s] %(name)s - %(message)s'
)

latest_event = None


class MyEventHandler:
    def on_call_invite(self, context, evt):
        global latest_event
        latest_event = evt
        print('[%s] on_call_invite' % evt.did)
        print('call-id:', evt.request.call_id)
        # print("%s" % evt.request)
        print('[%s] from: %s' % (evt.did, evt.request.from_))
        print('[%s] allows: %s' % (evt.did, evt.request.allows))
        print('[%s] contacts: %s' % (evt.did, evt.request.contacts))
        for hname in ('User-Agent',):
            print('[%s] header["%s"]: %s' % (evt.did, hname, evt.request.get_header(hname)))

    def on_call_cancelled(self, context, evt):
        global latest_event
        latest_event = evt
        print('[%s] call_cancelled' % evt.did)

    def on_call_closed(self, context, evt):
        global latest_event
        latest_event = evt
        print('[%s] call_closed' % evt.did)


initialize()
ctx = Context()
ctx.event_handler = MyEventHandler()
ctx.masquerade_contact('192.168.56.101', 5060)

print('listening...')
ctx.listen_on_address()
print('starting...')

ctx.start()
print('started!')

while True:
    s = sys.stdin.readline().strip().lower()
    if s in ('q', 'quit'):
        ctx.stop()
        break
    elif s == 'ack':
        with ctx.lock:
            ctx.call_send_ack(latest_event.did)
    elif s in ('t', 'terminate'):
        with ctx.lock:
            ctx.call_terminate(latest_event.cid, latest_event.did)
    elif s.isdecimal():
        status = int(s)
        if status == 200:
            with ctx.lock:
                msg = call.Answer(ctx, latest_event.tid, 200)
                msg.content_type = 'application/sdp'
                msg.set_body(
                    "v=0\r\n"
                    "o=jack 0 0 IN IP4 192.168.56.101\r\n"
                    "s=conversation\r\n"
                    "c=IN IP4 192.168.56.101\r\n"
                    "t=0 0\r\n"
                    "m=audio 54000 RTP/AVP 0 8 101\r\n"
                    "a=rtpmap:0 PCMU/8000\r\n"
                    "a=rtpmap:8 PCMA/8000\r\n"
                    "a=rtpmap:101 telephone-event/8000\r\n"
                )
                ctx.call_send_answer(answer=msg)
        else:
            with ctx.lock:
                ctx.call_send_answer(latest_event.tid, status)
