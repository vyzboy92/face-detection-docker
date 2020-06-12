FROM ubuntu:16.04
MAINTAINER vysakh@accubits.com

RUN apt-get update -y && apt-get install software-properties-common -y

RUN apt-get install -y build-essential python3 python3-dev python3-pip

RUN python3 -m pip install pip --upgrade && \
        python3 -m pip install wheel
	
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN pip install -U numpy \
	opencv-python \
	imutils\
	flask
	
RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf ~/.cache/pip

RUN mkdir face-demo

COPY . /face-demo

WORKDIR "face-demo"

RUN chmod +x face_app.py

ENTRYPOINT ["python3", "face_app.py"]
