FROM python:3.6-alpine3.7

RUN echo http://dl-cdn.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories; \
    apk update; \
    apk add --no-cache build-base python3-dev alpine-sdk libffi

ADD requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

CMD moto_server -p 3000 -H 0.0.0.0
