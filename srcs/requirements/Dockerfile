FROM --platform=$BUILDPLATFORM python:3.12-alpine

WORKDIR /chat

EXPOSE 8000

ENV PIP_ROOT_USER_ACTION ignore
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --update --no-cache --virtual build-deps gcc python3-dev musl-dev bash gcc libc-dev linux-headers postgresql-dev postgresql-client libffi-dev gettext

COPY main/ .

COPY start.sh .

COPY .env .

RUN pip3 install --upgrade pip && \
pip3 install -r requirements.txt --no-cache-dir
