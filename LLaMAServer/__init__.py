import socketio
from aiohttp import web
from PyLLaMA import PyLLaMA

app = web.Application()
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='aiohttp')
sio.attach(app)
llama = {
    'model': None
}
header = None
input = None

@sio.on('login')
def login(sid, data):
    if llama['model'] is None:
        return {}
    else:
        return {
            'header': header,
            'input': input,
        }

@sio.on('initialize')
def initialze_model(sid, data):
    if llama['model'] is not None:
        return {}
    header = data.get('header')
    input = data.get('input')
    llama['model'] = PyLLaMA(
        'models/GPT4All/gpt4all-lora-quantized-new.bin',
        header_text=header,
        prefix=input,
    )
    return {}

async def do_predict():
    n_remains = 512
    print('start predict')
    while n_remains > 0:
        next_str = llama['model'].predict_next()
        if next_str is None:
            break
        print(next_str, end='', flush=True)
    print('\n[End]')

@sio.on('predict')
def predict(sid, data):
    if llama['model'] is None:
        return {}
    sio.start_background_task(do_predict)
    return {}
