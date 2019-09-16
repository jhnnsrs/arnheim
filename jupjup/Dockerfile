FROM python:3.7

RUN mkdir -p /code
ADD . /code/

WORKDIR /code

# install dependencies

RUN apt-get update; apt-get install -y libncurses5-dev libreadline-dev libgsl0-dev
RUN pip install --no-cache-dir jupyterlab

# install neuron


RUN pip install -r requirements.txt

# Specify the default command to run
