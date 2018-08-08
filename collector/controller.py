from threading import Thread
import sys
import os

sys.path.append("/home/mike/workspace/IOT-Hotel-Room-Protection/collector")
from lib.cruncher import *
from flask import Flask
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
        self.app.run(host='0.0.0.0', port=5000)

    def register_routes(self):
        @self.app.route('/config')
        def hello_world():
            return 'Welcome to the configuration page of IOT-Hotel-Room-Protection device {}'.format(self.name)

        @self.app.route('/begin_collection/<thread_name>',methods = ['GET','POST'])
        def collector(thread_name):
            extractor = Thread(group=None, target=ingress, name=thread_name, args=(
                [],
                50, # How far behind will the moving average lag, larger the better
                3.5, # Number of standard deviations away from the moving average will cause a trigger
                1, # Influence of new point
                1, # Read frequency on the serial connection
                serial.Serial(sys.argv[0], 115200, timeout = 1),
                False,
                0,
                self.name
            ), kwargs={})
            collectors[thread_name] = extractor
            extractor.start()
            return 'Collection has started!'
        
        @self.app.route('/stop_collection/<thread_name>',methods = ['GET','POST'])
        def kill(thread_name):
            if thread_name in collectors.keys():
                collectors[thread_name].join()


if __name__ == "__main__":
    Collector()
    