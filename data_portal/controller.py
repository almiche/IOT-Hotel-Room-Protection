from threading import Thread
import sys
import os
from registry import *
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_hashing import Hashing
import secrets
from flask_cors import CORS,cross_origin
import logging

class Server():

    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.hashing = Hashing(self.app)
        CORS(self.app)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.register_routes()
        logging.basicConfig(level=logging.INFO)
        self.app.run(host='0.0.0.0', port=5000,debug=False)

    def register_routes(self):
        @self.app.route('/')
        @cross_origin()
        def index():
            return 'Welcome to the api v1.0',200

        @self.app.route('/api/v1.0/users',methods=['GET'])
        @self.app.route('/api/v1.0/users/<user>',methods=['GET','PUT'])
        @cross_origin(headers=['Content-Type'])
        def handle_users(user=None):
            if request.method == 'GET':
                if user is not None:
                    return jsonify(return_user(user))
            if request.method == 'PUT':
                if user is not None:
                    password = request.json['password']
                    salt = secrets.token_hex(nbytes=16)
                    hash = self.hashing.hash_value(password, salt=salt)
                    create_new_user(username=user,salt=salt,hash=hash)
                    return 'New user has been added',200
        
        @self.app.route('/api/v1.0/users/<user>/device/<device>',methods=['GET','PUT'])
        @self.app.route('/api/v1.0/users/<user>/device',methods=['GET'])
        @cross_origin(headers=['Content-Type'])
        def handle_devices(user, device = None):
            if request.method == 'GET':
                return jsonify(return_devices_for_user(user,device))
            if request.method == 'PUT':
                if device:
                    mac = device
                    device_type = request.json['device_type']
                    collector_version = request.json['collector_version']
                    room = request.json['room']
                    owner =request.json['owner']
                    create_new_device(mac,device_type,collector_version,room,owner)
                    # Add verification here
                    return 'New device has been added',200

        @self.app.route('/api/v1.0/users/<user>/device/<device>/Log/<log>',methods=['GET','PUT'])
        @self.app.route('/api/v1.0/users/<user>/device/<device>/Log',methods=['GET'])
        @cross_origin(headers=['Content-Type'])
        def handle_logs(user,device,log = None):
            if request.method == 'GET':
                return jsonify(return_logs_for_device(user,device,log))
            if request.method == 'PUT':
                if log:
                    log_dump = request.json['log_dump']
                    timestamp  = request.json['timestamp']
                    device = request.json['device']
                    create_new_log(log_dump,timestamp,device)
                    return 'Log added',200

if __name__ == "__main__":
    Server()
