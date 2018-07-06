FROM ubuntu

RUN apt-get update &&\
    apt-get -y install --no-install-recommends  python3 &&\
    apt-get -y install python3-pip git &&\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN pip3 install pipenv
RUN mkdir -p /usr/iot_door
WORKDIR /usr/iot_door
RUN git clone https://github.com/almiche/IOT-Hotel-Room-Protection.git .
RUN locale
RUN pipenv lock
RUN set -ex && pipenv install --deploy --system
RUN apt-get -y remove git python3-pip
RUN apt-get clean

CMD "echo Hello world!"
