import socketio

sio = socketio.Client()

header = """Letter from Justine."""
input = """Dear lady P."""


def predict_callback(result):
    print('Predict callback!')


def set_header_callback(result):
    print('Set header ok', result)
    sio.emit('predict', {
        'input': input
    }, callback=predict_callback)


def send_initialize_callback(result):
    print('Send initialize ok')
    sio.emit('set-header', {
        'header': header,
    }, callback=set_header_callback)


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


@sio.on('start-prediction')
def start_predict_event():
    print('[Start Prediction]')
    print(header)
    print(input)


@sio.on('predicted')
def predicted_event(data):
    print(data['next_str'], end='', flush=True)


@sio.on('stop-prediction')
def stop_prediction_event():
    print('\n[Stop Prediction]')


if __name__ == '__main__':
    sio.connect('http://localhost:8000')
    sio.wait()
