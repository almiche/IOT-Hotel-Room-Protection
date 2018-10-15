from threading import Thread
import sys
import os
from cruncher import *
from flask import Flask, render_template
import random
import threading
import requests
import serial
import sys


collectors = {}

class Collector():

    def __init__(self):
        print(sys.path)
        self.name = random.getrandbits(128)
        self.app = Flask(__name__)
        self.register_routes()
        self.thread_name = random.getrandbits(128)
        try:  
            self.serialport = os.environ.get("PORT")
            self.owner = os.environ.get("OWNER")
            self.mac = os.environ.get("MAC")
            self.data_portal = os.environ.get("PORTAL")
        except KeyError: 
            print("Not exist environment value for %s" % "key_maybe_not_exist")
        self.app.run(host='0.0.0.0', port=5000)

    def register_routes(self):
        @self.app.route('/config')
        def hello_world():
            return 'Welcome to the configuration page of IOT-Hotel-Room-Protection device {}'.format(self.name)

        @self.app.route('/begin_collection',methods = ['GET','POST'])
        def collector():
            self.extractor = Thread(group=None, target=ingress, name=self.thread_name, args=(
                [],
                50, # How far behind will the moving average lag, larger the better
                3.5, # Number of standard deviations away from the moving average will cause a trigger
                1, # Influence of new point
                1, # Read frequency on the serial connection
                serial.Serial(self.serialport, 115200, timeout = 1),
                20,
                0,
                self
            ), kwargs={})
            self.extractor.start()
            return 'Collection has started!',200
        
        @self.app.route('/stop_collection/<thread_name>',methods = ['GET','POST'])
        def kill(thread_name):
                self.extractor.join()
                return 'Collection has stopped',200


if __name__ == "__main__":
    Collector()
    