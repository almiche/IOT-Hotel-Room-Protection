from threading import Thread
import sys
import os

sys.path.append("/home/mike/workspace/IOT-Hotel-Room-Protection/collector")
print(sys.path)
from flask import Flask, render_template, request
from flask_socketio import SocketIO

collectors = {}

class Server():

    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.register_routes()
        self.app.run(host='0.0.0.0', port=5000)

    def register_routes(self):
        @self.app.route('/')
        def index():
            print()

        @self.app.route('/ingress',methods=['GET', 'POST'])
        def handle_ingress(message):
            if request.method == 'POST':
                print('Disruption recieved: ' + message + "from " + request.form['name'] + ": " + request.form['data'])


if __name__ == "__main__":
    Server()
