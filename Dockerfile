FROM python:3.6-slim

ENV PYTHONBUFFERED 1

RUN mkdir /code

ADD . /code
WORKDIR /code

RUN pip3 install -r requirements.txt
