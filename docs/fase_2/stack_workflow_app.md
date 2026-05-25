# Stack Docker y workflow

## Servicios

El stack principal esta en `containers/docker-compose.yml`.

- `n8n`: orquesta el workflow completo.
- `grobid`: convierte PDFs en XML TEI.
- `pipegrobid`: ejecuta el pipeline inicial de PipeGrobid.
- `python_runner`: ejecuta scripts Python llamados desde n8n con dependencias instaladas.
- `fuseki`: triplestore SPARQL para el KG.
- `research_api`: API FastAPI que consulta Fuseki.
- `research_frontend`: frontend Streamlit para explorar el KG.

## Prerrequisitos

- Docker Desktop levantado.
- PDFs colocados en `pdfs/`.
- `containers/.env` creado desde `containers/.env.example`.
- `GROQ_API_KEY` y `HF_TOKEN` si se ejecutan los pasos que usan LLM/HuggingFace.

## Levantar servicios

Primera ejecucion:

```bash
docker compose -f containers/docker-compose.yml up --build -d
```

Ejecuciones posteriores:

```bash
docker compose -f containers/docker-compose.yml up -d
```

URLs principales:

```text
n8n:              http://localhost:5678
research_api:     http://localhost:8000/docs
research_frontend http://localhost:8501
fuseki:           http://localhost:3030
```

## Ejecutar workflow

1. Abrir `http://localhost:5678`.
2. Importar `containers/workflow/pipegrobid_workflow.json`.
3. Entrar en `pipegrobid_workflow`.
4. Ejecutar el workflow manualmente.
5. Esperar a que termine el procesamiento y la carga del KG en Fuseki.
6. Abrir `http://localhost:8501`.
7. Pulsar `Actualizar datos` para limpiar cache de Streamlit.

El boton `Actualizar datos` no reconstruye el KG; solo fuerza al frontend a consultar de nuevo `research_api`.
