FROM debian:latest

RUN apt-get update &&\
    apt-get install -y python3 &&\
    apt-get install -y python3-flask &&\
    apt-get install -y python3-numpy &&\
    apt-get install -y python3-serial python3-requests

CMD ["python3","/collector/controller.py"]
