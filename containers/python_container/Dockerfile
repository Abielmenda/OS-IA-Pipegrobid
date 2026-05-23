# containers/python_runner/Dockerfile

FROM python:3.11-slim

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    bash \
    build-essential \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

ENV PYTHONPATH=/workspace
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV POETRY_VIRTUALENVS_PATH=/opt/poetry-venvs
ENV POETRY_CACHE_DIR=/opt/poetry-cache
ENV POETRY_NO_INTERACTION=1

WORKDIR /workspace

# Copiamos solo los ficheros de dependencias para aprovechar la cache de Docker
COPY assigment_2/step_2/xmls_parse/pyproject.toml assigment_2/step_2/xmls_parse/poetry.lock /workspace/assigment_2/step_2/xmls_parse/
COPY assigment_2/step_2/ner_extraction/pyproject.toml assigment_2/step_2/ner_extraction/poetry.lock /workspace/assigment_2/step_2/ner_extraction/
COPY assigment_2/step_3/topic_modeling/pyproject.toml assigment_2/step_3/topic_modeling/poetry.lock /workspace/assigment_2/step_3/topic_modeling/
COPY assigment_2/step_4/online_enrichment/pyproject.toml assigment_2/step_4/online_enrichment/poetry.lock /workspace/assigment_2/step_4/online_enrichment/
COPY assigment_2/step_4/gen_local_kg/pyproject.toml assigment_2/step_4/gen_local_kg/poetry.lock /workspace/assigment_2/step_4/gen_local_kg/

# Instalamos dependencias una vez, durante el build de la imagen
RUN set -e; \
    cd /workspace/assigment_2/step_2/xmls_parse && poetry install --no-root; \
    cd /workspace/assigment_2/step_2/ner_extraction && poetry install --no-root; \
    cd /workspace/assigment_2/step_3/topic_modeling && poetry install --no-root; \
    cd /workspace/assigment_2/step_4/online_enrichment && poetry install --no-root; \
    cd /workspace/assigment_2/step_4/gen_local_kg && poetry install --no-root

WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"] 
