FROM python:3.7.7-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y libpq-dev build-essential

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

RUN groupadd django && \
    useradd -g django django && \
    chown -R django:django /usr/src/app

USER django

EXPOSE 8000
