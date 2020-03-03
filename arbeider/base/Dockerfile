FROM python:3.7

# Install Minimal Dependencies for Django
ADD requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt

# Install Arbeid
RUN mkdir /code
ADD . /code
WORKDIR /code

