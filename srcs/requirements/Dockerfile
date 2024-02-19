FROM --platform=$BUILDPLATFORM python:3.10-alpine

WORKDIR /chat

EXPOSE 8000

ENV PIP_ROOT_USER_ACTION ignore
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && apk add bash
RUN apk add --virtual build-deps gcc python3-dev musl-dev && \
apk add postgresql-dev

COPY . .

RUN pip3 install --upgrade pip && \
  pip3 install -r main/requirements.txt --no-cache-dir
