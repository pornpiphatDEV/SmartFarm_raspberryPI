from flask import Flask, render_template

import json
from random import randrange
from flask import Flask, render_template
from flask_socketio import SocketIO
import json

# with open('setupsystem_control.json') as json_file:
#     data = json.load(json_file)
#     luxvalue_min = data['luxvalue_min']

import eventlet
eventlet.monkey_patch()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/controlpage')
def controlpage():
    return render_template('controlpage.html')


@app.route('/setingcontrolpage')
def setingcontrolpage():
    with open('setupsystem_control.json') as json_file:
        data = json.load(json_file)
        print(data)

    return render_template('setingcontrolpage.html', data=data)


@socketio.on('my event')
def handle_my_custom_event(json):

    print('received json: ' + str(json))


@socketio.on('connect')
def on_connect():
    print('Server received connection')


def dht22senser():
    while True:
        h = randrange(100)
        t = randrange(100)

        if h >= 50:
            socketio.emit('dht22_senser', {
                          'temperature':  t, 'humidity': h, "output_fan": 1})
            eventlet.sleep(1)
        else:
            socketio.emit('dht22_senser', {
                          'temperature':  t, 'humidity': h, "output_fan": 0})
            eventlet.sleep(1)


def lightsenser():
    while True:
        lux = randrange(100)
        if lux >= 50:
            socketio.emit('lightsenser', {'lux':  lux, 'curtain': 1})
            eventlet.sleep(1)
        else:
            socketio.emit('lightsenser', {'lux':  lux, 'curtain': 0})
            eventlet.sleep(1)


def soilmoisturesenser():
    while True:
        soilmoisture1 = randrange(100)
        soilmoisture2 = randrange(100)
        waterpump1 = 0
        waterpump2 = 0

        if soilmoisture1 >= 50:
            waterpump1 = 1
        if soilmoisture2 >= 50:
            waterpump2 = 1

        socketio.emit('soilmoisturesenser', {
                      'soilmoisture1':  soilmoisture1, 'soilmoisture2': soilmoisture2, "waterpump1": waterpump1, "waterpump2": waterpump2})
        eventlet.sleep(1)


eventlet.spawn(dht22senser)
eventlet.spawn(lightsenser)
eventlet.spawn(soilmoisturesenser)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
