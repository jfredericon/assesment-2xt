FROM python:3.7-stretch

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

RUN python manage.py migrate

CMD ["uwsgi", "app.ini"]