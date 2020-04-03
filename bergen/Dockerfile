FROM python:3.7
LABEL maintainer="jhnnsrs@gmail.com"


# install dependencies
# this needs to be installed due to opencv dependencies on graphical lbraries, why no idea?
ADD requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt


ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /code
WORKDIR /code

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000


