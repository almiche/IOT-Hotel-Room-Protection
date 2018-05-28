import os
import sys
import serial
import os
import sqlite3
import numpy as np
import time

def thresholding_algo(y, lag, threshold, influence):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
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
    while True:
        read_out = 0

        try:
            read_out = int(ser.readline().decode('utf-8'))
        except Exception as e:
            print(type(e))

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
        if(nth_point%(60/timeout) == 1 and nth_point > 1): # Dump data to mysqlite
            print("Database is currently at %s dumping" % len(db))
            '''
             Once a dump is being done, the last lag number of elements of the current list are moved to the front of the list 
             and the rest of the values are cleaned out this is in order for the moving average filter to still have values to lag behind with
             and compare against
            '''
            temp_lag_storage = db[-lag:]
            if spike_flag:
                spike_flag = False
                result = {
                    'spikes':result['signals'],
                    'raw_signals':db
                }
            # TODO: Dump data here
            db = temp_lag_storage