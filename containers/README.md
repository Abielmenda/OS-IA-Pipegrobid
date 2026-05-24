# Contenedores de generación del KG y APP

Este directorio contiene el `docker-compose.yml` usado para levantar el entorno completo para ejecución del workflow y levantamiento de la aplicación.

## Contenedores

- `n8n`: gestiona y ejecuta el workflow `pipegrobid_workflow`, parseando en XML con GROBID los pdfs y llamando a los scripts necesarios de cada step.
- `python_runner`: sirve únicamente para correr los scripts Python llamados desde n8n, con las dependencias necesarias ya instaladas.
- `fuseki`: mantiene el grafo de conocimiento en un triplestore para poder hacer consultas SPARQL.
- `research_api`: expone una API que consulta Fuseki y permite usar el KG desde nuestra app.
- `pipegrobid` y `GROBID` de la fase 1 (explicación en README.md de la raíz del proyecto)
## Prerrequisitos

Antes de levantar los contenedores:

- Copia `containers/.env.example` a `containers/.env` y rellena `GROQ_API_KEY` y `HF_TOKEN`.


## Ejecución

Desde `containers/`, la primera vez se debe construir y levantar todo con:

```bash
docker compose up --build -d
```

En las siguientes ejecuciones, si no se han cambiado Dockerfiles o dependencias, basta con:

```bash
docker compose up -d
```

Después se abre n8n en `http://localhost:5678` y se importa manualmente el workflow desde:

```text
containers/workflow/pipegrobid_workflow.json
```

Una vez importado, se entra en `pipegrobid_workflow` y se ejecuta manualmente.

