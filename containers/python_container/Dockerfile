# containers/python_runner/Dockerfile

FROM python:3.11-slim

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    bash \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

ENV PYTHONPATH=/workspace
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV POETRY_VIRTUALENVS_PATH=/opt/poetry-venvs
ENV POETRY_CACHE_DIR=/opt/poetry-cache

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"]