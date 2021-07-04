# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
LABEL maintainer="anlin.kong@gmail.com"

COPY . /blog
WORKDIR /blog
RUN pip3 --no-cache-dir install -U -r requirements.txt

ENV PORT=5000
ENV DB_CONNECTION

EXPOSE $PORT
RUN mkdir /etc/blogdemo/
VOLUME /etc/blogdemo/

CMD [ "python3", "blog/app.py"]