FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV REDIS_HOST "redis"
RUN mkdir /code
ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt
RUN pip install psycopg2


