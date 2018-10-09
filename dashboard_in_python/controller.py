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
import requests
import pry

class Server():

    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.hashing = Hashing(self.app)
        CORS(self.app)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.app.config['TEMPLATE_AUTO_RELOAD'] = True
        self.register_routes()
        self.app.run(host='0.0.0.0', port=5001,debug=True)

    def register_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/generate-token',methods=['POST'])
        def signin():
            pry()
            wush = request
            data = request.json
            r = requests.post("http://localhost:5000/api/v1.0/generate-token", json=data)
            print(r.text)
            pry()
            return jsonify(r.json()),200

        @self.app.route('/signout',methods=['POST'])
        def signout():
            data = request.json
            r = requests.post("http://localhost:5000/api/v1.0/signout", json=data)
            return jsonify(r.json()),r.status_code

        @self.app.route('/users/<user>',methods=['PUT'])
        def handle_users(user):
            if request.method == 'PUT':
                r = requests.put("http://localhost:5000/api/v1.0/users/{}".format(user),json=request.json)
                return jsonify(r.json()),r.status_code
        
        @self.app.route('/users/<user>/device',methods=['GET','PUT'])
        def handle_devices(user):
            if request.method == 'GET':
                r = requests.get("http://localhost:5000/api/v1.0/users/{}/device?token={}".format(user,request.args['token']))
                return jsonify(r.json()),r.status_code
            if request.method == 'PUT':
                r =  requests.put("http://localhost:5000/api/v1.0/users/{}/device".format(user),json=request.json)
                return jsonify(r.json()),r.status_code

        @self.app.route('/users/<user>/logs',methods=['GET'])
        def handle_logs(user,device=None):
            if request.method == 'GET':
                r = requests.get("http://localhost:5000/api/v1.0/users/{}/logs?token={}".format(user,request.args['token']))
                return jsonify(r.json()),r.status_code
        # Add all other routes here

if __name__ == "__main__":
    Server()
