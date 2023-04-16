import socketio
from aiohttp import web
from asgiref.sync import sync_to_async

from PyLLaMA import PyLLaMA

app = web.Application()
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='aiohttp')
sio.attach(app)

llama: dict[str, PyLLaMA] = {}


@sio.event()
def connect(sid, environ):
    print('connect', sid)


@sio.event()
def disconnect(sid):
    if sid in llama:
        del llama[sid]
    print('disconnect', sid)


@sio.on('login')
def login(sid, data):
    if sid not in llama:
        return {}
    else:
        return {}


@sio.on('initialize')
def initialze_model(sid, data):
    if sid in llama:
        return {}
    llama[sid] = PyLLaMA(
        'models/GPT4All/gpt4all-lora-quantized-new.bin',
    )
    llama[sid].set_header(
        'Below is an instruction that describes a task. Write a response that appropriately completes the request.',
    )
    return {
        'header': llama[sid].header,
    }


@sio.on('set-header')
def set_header(sid, data):
    if sid not in llama:
        return {}
    header = data.get('header')
    if header is None:
        return {}
    llama[sid].set_header(header)
    return {
        'header': llama[sid].header,
    }


async def do_predict(sid, user_input: str):
    n_remains = 512
    await sio.emit('start-prediction', to=sid)
    print('start predict')
    user_input and print(user_input, end='', flush=True)
    async_predict = sync_to_async(llama[sid].predict_next)
    while n_remains > 0:
        next_str = await async_predict()
        if next_str is None:
            break
        await sio.emit('predicted', {
            'next_str': next_str,
        }, to=sid)
        print(next_str, end='', flush=True)
        n_remains -= 1
    await sio.emit('stop-prediction', to=sid)
    print('\n[End]')


@sio.on('predict')
def predict(sid, data):
    if sid not in llama:
        return {}
    user_input = data.get('input')
    if user_input is not None:
        llama[sid].send_input(user_input)
    sio.start_background_task(do_predict, sid, user_input)
    return {}
