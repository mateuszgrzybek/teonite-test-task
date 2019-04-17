FROM python:3.6-alpine

ADD requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt

ADD . /app

CMD python manage.py migrate \
    python manage.py makemigrations\
    python manage.py migrate \
    python manage.py runserver 0.0.0.0:8080
