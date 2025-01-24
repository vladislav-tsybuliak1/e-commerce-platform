FROM python:3.12.7-alpine3.20

LABEL maintainer="vladislav.tsybuliak@gmail.com"

RUN pip install poetry==2.0.1

ENV PYTHONBUFFERED 1

WORKDIR app/

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

