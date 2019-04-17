FROM python:3.6-alpine

ENV PYTHONUNBUFFERED=1

ADD requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ADD . /app

CMD ['python3','connect.py']
