FROM python:3.11-slim

WORKDIR /app

# Evita que Python genere __pycache__ y mejora logs en Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala Poetry
RUN pip install --no-cache-dir poetry

# Instala dependencias primero para aprovechar la cache de Docker
COPY pyproject.toml poetry.lock /app/

# Instala las dependencias dentro del entorno global del contenedor
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Copia el código de la API
COPY . /app/

# Expone el puerto de FastAPI
EXPOSE 8000

# Arranca el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]