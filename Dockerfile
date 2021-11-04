# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
LABEL maintainer="anlin.kong@gmail.com"

COPY . /blog
WORKDIR /blog
RUN pip3 --no-cache-dir install -U -r requirements.txt

ENV PORT=5000
ENV DB_CONNECTION=

RUN mkdir /etc/blog/
VOLUME /etc/blog/

EXPOSE $PORT
CMD [ "python3", "blog/app.py"]