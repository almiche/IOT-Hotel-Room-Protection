from threading import Thread
import sys
import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_hashing import Hashing
import secrets
from flask_cors import CORS,cross_origin

class Server():

    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.hashing = Hashing(self.app)
        CORS(self.app)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.app.config['TEMPLATE_AUTO_RELOAD'] = True
        self.register_routes()
        self.app.run(host='0.0.0.0', port=5000,debug=True)

    def register_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

if __name__ == "__main__":
    Server()
