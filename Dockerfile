FROM python:3.10.8-slim

RUN apt-get update  \
    && apt-get install -y python3-dev libpq-dev gcc curl

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /opt/src
WORKDIR /opt/src

COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements-dev.txt
RUN rm requirements.txt
RUN rm requirements-dev.txt

COPY src .
# COPY .env ../.env
COPY ./dump.json .

EXPOSE 8890

# CMD python manage.py runserver 0.0.0.0:8890