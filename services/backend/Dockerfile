FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY /src .