
![Docker Pulls](https://img.shields.io/docker/pulls/mashape/kong.svg?style=for-the-badge)  
[![Docker Hub repository](http://dockeri.co/image/almiche/iot_hotel)](https://registry.hub.docker.com/u/almiche/iot_hotel/)

# IOT-Hotel-Room-Protection
ESP8266 based project for securing hotel rooms

## Why do I need this ?

This hardware hack enables hotel goers to monitor when their hotel room door has been opened in order to provide piece of mind while travelling. It will all be housed in a covert shell disguised as a "do not disturb" sign providing discretion to the user. 

## How it's all done

This hack utilises the esp 8266 platform mated with an accelerometer, which if all goes well will be housed in a 3d printed encolsure on top of which a do not disturb sign will be clipped on. This hardware will be working in symphony with a sinatra webserver which will host the user interface for the client side of the hardware hack displaying different updates about the status of the sign.

## What has been done so far ?

### Februrary 20th 2018 Update 1

So far the scripting part of the hack for the esp microcontroller is being worked on and tweaked. The most difficult part is tweaking the accelerometer and making sur it's properaly sensitized. I have also started work on the backend api services for logging all the data coming. I have also started to look into simple 3d modelling software as potential candidates for creating the enclosure.

I have started designing the 3d component and will be posting regular updates of my progress.
![alt text](https://raw.githubusercontent.com/almiche/IOT-Hotel-Room-Protection/master/wushy.PNG)

### February 22nd 2018 New design

| ![alt text](https://github.com/almiche/IOT-Hotel-Room-Protection/blob/master/3dRender_1.PNG?raw=true)  |![alt text](https://github.com/almiche/IOT-Hotel-Room-Protection/blob/master/Capture.PNG?raw=true) |
|---|---|

### October 15 2018

It's been quite a while since the last update and I have had some long hiatuses. 

| ![alt text](https://github.com/almiche/IOT-Hotel-Room-Protection/blob/master/bump.gif?raw=true)  |![alt text](https://github.com/almiche/IOT-Hotel-Room-Protection/blob/master/dashboard.png?raw=true) |
|---|---|

For the last 2 weeks I have pushing hard into making this project a reality. Alot has happened since the last update so a rundown is in order. First the application is segmented into main parts the frontend ui and the backend app which communicates with the database. All of this is  containzeried and orchestrated runnning in a three node cluster kubernetes instance in google cloud (because the two end users of this system really need high availbility ). The system is designed  to be completely stateless in order to run correctly in a distributed scenario any stateful data is stored in MySQL.

The hardware  part of this project is also complete I have 3d printed the shell and attached a rasberry pi zero w paired with an esp8285 and an adxl345 accelerometer all with unsoldered headers. A little soldering here and there and some double sided and it was all to go. The device is running a flask app in its main thread in order to allow simple controls via REST API to the device. In the secondary thread is the actual algorithm which does real time peak detection by comparing the distance of the current  point from the moving average to the current standard deviation multiplied by a multiple of standard deviations known as the threshold. It then proceeds to POST to the one of the three flask containers in the cloud.

![alt text](https://github.com/almiche/IOT-Hotel-Room-Protection/blob/master/innards.jpg?raw=true)

I have also implmented a login system whihch allows users to create accounts and add their own door hanger units in order to log !

There is still some work to be done in the way of optimization and cleanup. I would also like to add web socket communication with the ui in order to lower the size of the payload being queried by AJAX (don't ask how large they are at the moment) If you have any questions feel free to ask. I will update  this  article in the future when I make any changes !

### Famingo Labs 2018
