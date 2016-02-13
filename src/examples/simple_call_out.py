import sys
import logging.config

from exosip2ctypes import initialize, Context, call


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

logging.info('startup!!!!')

initialize()
ctx = Context(contact_address=('192.168.56.101', 5060))

latest_event = None


def on_call_ack(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_ack' % evt.did)


def on_call_invite(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_invite' % evt.did)
    # print("%s" % evt.request)
    print('[%s] from: %s' % (evt.did, evt.request.from_))
    print('[%s] allows: %s' % (evt.did, evt.request.allows))
    print('[%s] contacts: %s' % (evt.did, evt.request.contacts))
    for hname in ('User-Agent',):
        print('[%s] header["%s"]: %s' % (evt.did, hname, evt.request.get_header(hname)))


def on_call_cancelled(evt):
    global latest_event
    latest_event = evt
    print('[%s] call_cancelled' % evt.did)


def on_call_closed(evt):
    global latest_event
    latest_event = evt
    print('[%s] call_closed' % evt.did)


def on_call_answered(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_answered' % evt.did)
    # print('%s' % evt.response)


def on_call_requestfailure(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_requestfailure' % evt.did)


def on_call_ringing(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_ringing' % evt.did)


def on_call_noanswer(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_noanswer' % evt.did)


def on_call_proceeding(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_proceeding' % evt.did)


def on_call_serverfailure(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_serverfailure' % evt.did)


def on_call_released(evt):
    global latest_event
    latest_event = evt
    print('[%s] on_call_released' % evt.did)


ctx.on_call_invite = on_call_invite
ctx.on_call_cancelled = on_call_cancelled
ctx.on_call_closed = on_call_closed
ctx.on_call_answered = on_call_answered
ctx.on_call_ack = on_call_ack
ctx.on_call_requestfailure = on_call_requestfailure
ctx.on_call_ringing = on_call_ringing
ctx.on_call_noanswer = on_call_noanswer
ctx.on_call_proceeding = on_call_proceeding
ctx.on_call_serverfailure = on_call_serverfailure
ctx.on_call_released = on_call_released

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
    elif s in ('m', 'makecall'):
        with ctx.lock:
            invite = call.InitInvite(ctx, 'sip:192.168.56.1', 'sip:example@192.168.56.101')
            invite.allows = ['INVITE', 'ACK', 'CANCEL', 'OPTIONS', 'BYE', 'REFER', 'NOTIFY', 'MESSAGE', 'SUBSCRIBE',
                             'INFO', 'UPDATE']
            invite.set_header('Supported', 'outbound')
            invite.content_type = "application/sdp"
            invite.set_body(
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
            # print("%s" % invite)
            ctx.call_send_init_invite(invite)
