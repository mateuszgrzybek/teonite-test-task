FROM python:3.6

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
ADD requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ADD . /app

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.0/wait /wait
RUN chmod +x /wait

CMD /wait && \
    python3 connect.py
