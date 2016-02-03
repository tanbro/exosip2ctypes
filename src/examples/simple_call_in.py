import sys

from exosip2ctypes import load, Context, Answer

load()
ctx = Context()

latest_event = None


def on_call_invite(evt):
    global latest_event
    latest_event = evt
    print('on_call_invite')

ctx.on_call_invite = on_call_invite

ctx.listen_on_address(address='192.168.56.101')
ctx.start()

while True:
    s = sys.stdin.readline().strip().lower()
    if s in ('q', 'quit'):
        ctx.stop()
        break
    elif s == 'ack':
        with ctx.lock:
            ctx.call_send_ack(latest_event.did)
    elif s.isdecimal():
        status = int(s)
        if s == 200:
            with ctx.lock:
                msg = Answer(ctx, latest_event.tid, 200)
                ctx.call_send_answer(latest_event.tid, msg)
        else:
            with ctx.lock:
                ctx.call_send_answer(latest_event.tid, int(s))

