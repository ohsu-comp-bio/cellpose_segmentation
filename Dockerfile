FROM python:3.8-slim

ENV CELLPOSE_VERSION=0.7.3 NUMBA_CACHE_DIR=/tmp
RUN apt-get update && \
    apt-get install -y --no-install-recommends git unzip wget &&\
    apt-get clean

RUN pip install -U pip && \
    pip install --no-cache-dir cellpose==$CELLPOSE_VERSION 'scikit-learn>1.0, <1.1' 'opencv-python-headless==4.5.1.48' 'scikit-image>0.17, <0.19'
