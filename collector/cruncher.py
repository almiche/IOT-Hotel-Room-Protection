import os
import sys
import serial
import os
import numpy as np
import time
import requests
import datetime

def thresholding_algo(y, lag, threshold, influence):
    signals = np.zeros(len(y)) # Build array of zeros to hold signals
    filteredY = np.array(y) # Insert current points in another array
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag]) # Calculate the average of the lag data points
    stdFilter[lag - 1] = np.std(y[0:lag])  # Calculate std dev of the lag data points
    for i in range(lag, len(y)):    # Going from lag to the end
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:    
            # If point's distance to the moving average is larger than the threshhold * the moving std dev
            # then flag this point
            if y[i] > avgFilter[i-1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))


def ingress(    db ,
                lag, # How far behind will the moving average lag, larger the better
                threshold, # Number of standard deviations away from the moving average will cause a trigger
                influence, # Influence of new point
                timeout, # Read frequency on the serial connection
                ser,
                spike_flag ,
                nth_point,
                app):
    while True:
        read_out = read_accelerometer(ser)

        db.append(read_out)
        nth_point += 1
        print("Point is currently %s and list is currently at %s" % (read_out,nth_point))

        if nth_point > lag: # Collect data points for the moving average filter lag
            result = (thresholding_algo(db,lag,threshold,influence))
            if(abs(result['signals'][-1]) == 1): # Spike detected
                spike_flag = True
                print("Motion detected!")
            pass
        else:
            print("Calibrating %d seconds remaining ..." % (lag - nth_point))
            print(db)
        if(nth_point%(10/timeout) == 1 and nth_point > 1): # Dump data
            '''
             Once a dump is being done, the last lag number of elements of the current list are moved to the front of the list 
             and the rest of the values are cleaned out this is in order for the moving average filter to still have values to lag behind with
             and compare against
            '''
            temp_lag_storage = db[-lag:]
            if spike_flag:
                spike_flag = False
                # Adding some extra data in order to have a nicer graph and stop detection for a bit after a spike
                for current in range(0:spike_flag): 
                    db.append(read_accelerometer(ser))
                result = {
                    'spikes':result['signals'],
                    'raw_signals':db
                }
                # TODO: Dump data here
                print(str(db))
                r = requests.put("{}/api/v1.0/users/{}/device/{}/logs".format(app.portal,app.owner,app.mac), json={
                                                                        'log_dump':str(db[0:40]),
                                                                        'timestamp': str(datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")),   
                                                                        })
                print(r.text)
            db = temp_lag_storage

def read_accelerometer(ser):
    try:
        read_out = int(ser.readline().decode('utf-8'))
    except Exception as e:
        print(type(e))
    return read_out

if __name__ == "__main__":
    # Port should be passed in as a config
    db = []
    lag = 50 # How far behind will the moving average lag, larger the better
    threshold = 3.5 # Number of standard deviations away from the moving average will cause a trigger
    influence = 1 # Influence of new point
    timeout = 1 # Read frequency on the serial connection
    ser = serial.Serial("/dev/cu.wchusbserial14510", 115200, timeout = 1)
    spike_flag = False
    nth_point = 0 # Tracks which collection point we're at since list db is being dumped every few minutes