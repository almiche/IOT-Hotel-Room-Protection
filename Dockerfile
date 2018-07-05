FROM ubuntu:latest

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install git
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN pip3 install pipenv
RUN mkdir -p /usr/iot_door
WORKDIR /usr/iot_door
RUN git clone https://github.com/almiche/IOT-Hotel-Room-Protection.git .
RUN locale
RUN pipenv lock
RUN set -ex && pipenv install --deploy --system
