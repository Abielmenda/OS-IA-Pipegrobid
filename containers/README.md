# Contenedores de generacion del KG y app

El detalle del stack Docker, ejecucion del workflow n8n, levantamiento de la app, API y frontend esta fusionado en la documentacion principal de la aplicacion:

- [App Knowledge Graph](../app.md)
- [Documentacion FASE 2](../docs/fase_2/index.md)

Resumen rapido:

```bash
docker compose -f containers/docker-compose.yml up --build -d
```

Despues:

- n8n: `http://localhost:5678`
- API: `http://localhost:8000/docs`
- Frontend: `http://localhost:8501`
