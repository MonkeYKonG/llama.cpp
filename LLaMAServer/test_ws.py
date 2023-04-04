import socketio

sio = socketio.Client()

def predict_callback(result):
    print('Predict callback!')

def send_initialize_callback(result):
    print('Send initialize ok')
    sio.emit('predict', {}, callback=predict_callback)

def send_initialize():
    sio.emit('initialize', {
        'header': 'Transcription of dialog',
        'input': 'Bob: Hello!\n',
    }, callback=send_initialize_callback)

def prepare_model_callback(result):
    print('Prepare moodel ok', result)
    sio.start_background_task(send_initialize)

def prepare_model():
    sio.emit('login', {}, callback=prepare_model_callback)

@sio.event
def connect():
    print("I'm connected!")
    sio.start_background_task(prepare_model)


@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect('http://localhost:8000')
sio.wait()