FROM python:3.7-alpine

WORKDIR /app

ADD . /app

RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	; \
	pip install -r requirements.txt; \
	apk del .build-deps;

CMD ["uwsgi", "app.ini"]