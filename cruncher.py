import os
import sys
import serial
import os
import sqlite3
import numpy as np

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
    ser = serial.Serial("/dev/cu.wchusbserial14510", 115200, timeout=1)
    db = []
    lag = 15 # How far behind will the moving average lag, larger the better
    threshold = 3.5 # Number of standard deviations away from the moving average will cause a trigger
    influence = 1 # Influence of new point
    while True:
        read_out = 0
        try:
            read_out = int(ser.readline().decode('utf-8'))
        except Exception as e:
            print(type(e))
        db.append(read_out)
        print("Point is currently %s and list is currently at %s" % (read_out,len(db)))
        if len(db) > lag:
            result = (thresholding_algo(db,lag,threshold,influence))['signals']
            if(result[-1] == 1):
                print("Spike!")
            pass
        else:
            print("herer")
            print(db)
   

