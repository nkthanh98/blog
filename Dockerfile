FROM python:3.6.8-alpine

EXPOSE 8000

WORKDIR /app

ADD ./requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

ADD . .

ENTRYPOINT gunicorn wsgi:application
