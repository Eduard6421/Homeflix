FROM python:3.10.5-bullseye
LABEL maintainer="eduard6421"


ARG DEV=false

ENV PYTHONBUFFERED 1

EXPOSE 8000

COPY ./Pipfile /tmp/Pipfile
COPY ./Pipfile.lock /tmp/Pipfile.lock

WORKDIR /tmp/

RUN apt-get update -y

RUN pip install --upgrade pip && pip install pipenv

RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev python-dev && \
    if [ $DEV = true ]; \
    then \
    pipenv install --dev --system; \
    else \
    pipenv install --system;\
    fi && \
    rm -rf /tmp/ && \
    echo "def1" && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

WORKDIR /app/

USER django-user
