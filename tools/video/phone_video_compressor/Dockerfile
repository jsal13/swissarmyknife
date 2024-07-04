FROM python:3.10.12-alpine3.18

WORKDIR /app

RUN apk add --no-cache ffmpeg

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./compressor.py compressor.py

RUN mkdir -p /app/videos
