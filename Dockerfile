# the docker image to be used
FROM python:3.6-alpine

# set python output straight to terminal without buffering first
ENV PYTHONUNBUFFERED 1

# create root directory for the project
RUN mkdir /samstagram

# set working directory to /samstagram
WORKDIR /samstagram

# copy project content to the container /samstagram
ADD . /samstagram/

RUN apk add --no-cache bash 

# insatll the required packages
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt
