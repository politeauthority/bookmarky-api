# Set the Docker registry URL
ARG DOCKER_REGISTRY="docker.io/library"

# Use the official Python 3.10 image with Alpine 3.16 as the base image
FROM ${DOCKER_REGISTRY}/python:3.11-alpine3.16 as base

ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app/

# Copy the local src directory to the working directory in the container
ADD ./build-files/pyproject.toml /app/
ADD ./build-files/tox.ini /app/
ADD ./build-files/src /app/
ADD ./scripts/install-polite-lib.sh /app

# Set environment variables
ENV LIB_DIR="/root"
# ENV POLITE_LIB_BRANCH="main"

# Install apk requirements
RUN apk add --update --no-cache --virtual .build-deps \
    gcc libc-dev linux-headers bash git \
    && apk add --no-cache libffi-dev \
    && apk add --no-cache --update --virtual .runtime-deps libgcc libstdc++ ca-certificates postgresql-dev gcc python3-dev musl-dev

# Shitty polite-lub install
RUN /app/install-polite-lib.sh \
    && apk add git \
    && apk del .build-deps

RUN cd /app/ && pip install .

CMD ["gunicorn", "web-app:app", "--chdir", "/app/bookmarky/api", "--bind=0.0.0.0:80"]

# Development container tools
FROM base as dev

RUN apk add bash curl vim

RUN pip install -r /app/requirements-dev.txt && mkdir /work
WORKDIR /work/

ADD build-files/tests /work/tests
# RUN cd /work/tests/ python3 /work/tests/setup.py build && python3 /work/tests/setup.py install
