FROM debian:latest

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update &&\
    apt-get install -y python3 &&\
    apt-get install -y python3-pip &&\
    apt-get install -y python-numpy python-scipy python-matplotlib &&\
    pip3 install flask

RUN apt-get install -y libatlas3-base &&\
    pip3 install pyserial &&\
    pip3 install numpy -i https://www.piwheels.hostedpi.com/simple &&\
    pip3 install requests       

CMD ["python3","/app/controller.py"]
