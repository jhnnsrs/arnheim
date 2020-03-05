FROM python:3.7

RUN apt-get install -y git

# Install Oracle Java 8
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME
ADD requirements.txt /tmp
WORKDIR /tmp

# install dependencies
# this needs to be installed due to opencv dependencies on graphical lbraries, why no idea?
RUN apt install -y libsm6 libxext6 libxrender-dev
RUN apt-get install -y gcc
RUN apt-get install -y build-essential
RUN pip install -vU setuptools
RUN pip install -vU numpy
RUN pip install -r requirements.txt


ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
RUN mkdir /code
ADD . /tmp
WORKDIR /code


