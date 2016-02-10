import sys

from exosip2ctypes import initialize, Context, Answer

initialize()
ctx = Context(contact_address=('192.168.56.101', 5060))
ctx.masquerade_contact('192.168.56.101', 5060)

latest_event = None


def on_call_invite(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_invite' % evt.did)
    # print("%s" % evt.request)
    print('[%s] from: %s' % (evt.did, evt.request.from_))
    print('[%s] allows: %s' % (evt.did, evt.request.allows))
    print('[%s] contacts: %s' % (evt.did, evt.request.contacts))
    for hname in ('User-Agent', ):
        print('[%s] header["%s"]: %s' % (evt.did, hname, evt.request.get_header(hname)))


def on_call_cancelled(evt):
    global latest_event
    latest_event = evt
    print('[%s] call_cancelled' % evt.did)


def on_call_closed(evt):
    global latest_event
    latest_event = evt
    print('[%s] call_closed' % evt.did)


ctx.on_call_invite = on_call_invite
ctx.on_call_cancelled = on_call_cancelled
ctx.on_call_closed = on_call_closed


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
    elif s == 'term':
        with ctx.lock:
            ctx.call_terminate(latest_event.cid, latest_event.did)
    elif s.isdecimal():
        status = int(s)
        if status == 200:
            with ctx.lock:
                msg = Answer(ctx, latest_event.tid, 200)
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
                ctx.call_send_answer(message=msg)
        else:
            with ctx.lock:
                ctx.call_send_answer(latest_event.tid, status)

