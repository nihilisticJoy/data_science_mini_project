FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

ENV FLASK_ENV=production

WORKDIR /app/app

CMD gunicorn app:server -b 0.0.0.0:8080 --log-level info
