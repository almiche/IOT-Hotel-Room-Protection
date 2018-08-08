FROM alpine:3.8

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8


COPY . /usr/iot_door
COPY Pipfile .
COPY Pipfile.lock .

WORKDIR /usr/iot_door/app

ADD repositories /etc/apk/repositories

RUN apk add --update python python-dev gfortran py-pip build-base py-numpy@community python3 &&\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* &&\
    pip3 install --no-cache-dir --upgrade pip &&\
    which python3 && python3 --version &&\
    pip3 install pipenv &&\
    export PIPENV_TIMEOUT=500 &&\
    pipenv lock &&\
    set -ex && pipenv --python /usr/bin/python3 install --deploy --system  &&\
    rm -rf /var/cache/* &&\
    rm -rf /root/.cache/*


CMD ["python3","controller.py"]
