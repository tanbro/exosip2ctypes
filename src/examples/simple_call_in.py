from exosip2ctypes import load, Context, AnswerMessage

load()
ctx = Context()


def on_call_invite(evt):
    with ctx.lock:
        answer_message = AnswerMessage(evt.tid, 404)
        ctx.send_answer_with_message(answer_message)

ctx.on_call_invite = on_call_invite

ctx.run()
