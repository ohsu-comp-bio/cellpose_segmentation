FROM ubuntu:20.04

ENV VERSION=0.6
RUN apt-get update && \
    apt-get install -y git python3 python3-pip unzip wget && \
    ln -s /usr/bin/python3 /usr/bin/python

RUN pip install cellpose==$VERSION opencv-python-headless==4.5.1.48 scikit-image==0.17.2 matplotlib==3.3.3