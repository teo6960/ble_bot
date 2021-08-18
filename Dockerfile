FROM phusion/baseimage

RUN apt-get update -q && \
    apt-get install -y vim git python3-dev python3-setuptools python3-apt build-essential python-dateutil python3-pip && \
    apt-get install -y
    
