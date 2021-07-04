FROM python:3.8-slim-buster
LABEL maintainer="Lingxian Kong"

ENV PORT=5000
ENV DB_CONNECTION=mysql+pymysql://root:zswgwsWzkwdHc11uhovZJ9ExOT8fmVhTu3Dj@10.0.17.9/blog?charset=utf8

COPY . /blog
WORKDIR /blog
RUN pip3 --no-cache-dir install -U -r requirements.txt

RUN mkdir /etc/blogdemo/
VOLUME /etc/blogdemo/

EXPOSE $PORT
CMD [ "python3", "blog/app.py"]