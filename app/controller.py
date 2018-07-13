from threading import Thread
import sys
import os

sys.path.append("/home/mike/workspace/IOT-Hotel-Room-Protection/app")
print(sys.path)
from lib.cruncher import *
from flask import Flask

collectors = {}

def register_routes(app):
    @app.route('/config')
    def hello_world():
        return 'Welcome to the configuration page of IOT-Hotel-Room-Protection device {}'.format("HS87DFDS878")

    @app.route('/begin_collection/<thread_name>',methods = ['GET','POST'])
    def collector(thread_name):
        extractor = Thread(group=None, target=ingress, name=thread_name, args=(



        ), kwargs={})
        collectors[thread_name] = extractor
        extractor.start()
        return 'Collection has started!'
    
    @app.route('/stop_collection/<thread_name>',methods = ['GET','POST'])
    def kill(thread_name):
        if thread_name in collectors.keys():
            collectors[thread_name].join()


if __name__ == "__main__":
    print(sys.path)
    app = Flask(__name__)
    register_routes(app)
    app.run(host='0.0.0.0', port=80)
    