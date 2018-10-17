from threading import Thread
import sys
import os
from registry import *
from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_hashing import Hashing
import secrets
from flask_cors import CORS,cross_origin
import logging
import pry

def start():
    CORS(app,expose_headers='Authorization')
    app.config['SECRET_KEY'] = 'secret!'
    app.config['TEMPLATE_AUTO_RELOAD'] = True
    register_routes()
    app.run(host='0.0.0.0', port=5000,debug=True)

def authenticate(user,request):
    if request.method == 'GET':
        if not request.args.get('token'):
            return False
        token = request.args.get('token')
    if request.method == 'PUT' or request.method == 'POST':
        if not request.json.get('token'):
            return False
        token = request.json['token']
    print(return_user(user))
    if check_login(user) and return_user(user)['api_token'] == token:
        return True
    else:
        return False

def register_routes():
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response 

    @app.route('/api/v1.0/generate-token',methods=['POST']) # Upon login return a new token if one doesnt exists
    def handle_transaction_tokenize():
        if request.method == 'POST':
            user = request.json['user']
            password = request.json.get('password',None)
            if password:
                salt = return_user(user)['salt']
                pass_hash = return_user(user)['password_hash']
                hash = hashing.hash_value(password, salt=salt)
                if pass_hash == hash:
                    if check_login(user):
                        return jsonify({'status':'logged','token':check_login(user),'user':user}),200
                    else:
                        api_token = secrets.token_hex(nbytes=120)
                        add_new_api_token(user,api_token)
                        return jsonify({'status':'logged','token':api_token,'user':user}),200
                else:
                    return jsonify({'status':'invalid'}),400
            else:
                return jsonify({'status':'No password provided'}),400

    @app.route('/api/v1.0/signout',methods=['POST'])
    def handle_sign_out():
        if request.method == 'POST':
            user = request.json['user']
            delete_api_token(user)
            return jsonify({'status':'OK'}),200

    @app.route('/api/v1.0/users/<user>',methods=['GET','PUT'])
    @cross_origin(headers=['Content-Type'])
    def handle_users(user):
        if request.method == 'GET':
            if authenticate(user,request):
                response = return_user(user)
                return jsonify(response),200
            else:
                return jsonify({'status':'You are not authorized to view this content'}),200
        if request.method == 'PUT':
            password = request.json['password']
            salt = secrets.token_hex(nbytes=16)
            hash = hashing.hash_value(password, salt=salt)
            create_new_user(username=user,salt=salt,hash=hash)
            return 'New user has been added',200
        
    @app.route('/api/v1.0/users/<user>/device',methods=['GET','PUT'])
    @cross_origin(headers=['Content-Type'])
    def handle_devices(user):
        if authenticate(user,request):
            if request.method == 'GET':
                response = {}
                response['devices'] = return_devices_for_user(user)
                return jsonify(response),200
            if request.method == 'PUT':
                mac = request.json['mac']
                device_type = request.json['device_type']
                collector_version = request.json['collector_version']
                room = request.json['room']
                owner =user
                create_new_device(mac,device_type,collector_version,room,owner)
                # Add verification here
                return jsonify({'status':'New device has been added'}),200
        else:
            return jsonify({'status':'You are not authorized to view this content'}),200

    @app.route('/api/v1.0/users/<user>/device/<device>/logs',methods=['PUT'])
    @app.route('/api/v1.0/users/<user>/logs',methods=['GET'])
    @cross_origin(headers=['Content-Type'])
    def handle_logs(user,device=None,log = None):
            if request.method == 'GET':
                if authenticate(user,request):
                    response = return_logs_for_user(user)
                    return jsonify(response),200
                else:
                    return jsonify({'status':'You are not authorized to view this content'}),200
            if request.method == 'PUT':
                    log_dump = request.json['log_dump']
                    timestamp  = request.json['timestamp']
                    device = device
                    return create_new_log(log_dump,timestamp,device)

        

if __name__ == "__main__":
    app = Flask(__name__)
    hashing = Hashing(app)
    start()
