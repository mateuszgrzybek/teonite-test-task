FROM python:3.6

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip3 install -r requirements.txt

ADD . /app

CMD ['python3','connect.py']
