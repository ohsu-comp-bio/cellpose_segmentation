FROM python:3.8-slim

ENV VERSION=0.7.2 NUMBA_CACHE_DIR=/tmp
RUN apt-get update && \
    apt-get install -y git unzip wget 

RUN pip install cellpose==$VERSION 'scikit-learn>1.0, <1.1' 'opencv-python-headless==4.5.1.48' 'scikit-image>0.17, <0.19'