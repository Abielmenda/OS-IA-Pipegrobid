# Workflow con n8n

## Prerrequisitos

Antes de levantar los contenedores, prepara estos ficheros:

1. Copia `containers/.env.example` a `containers/.env` y rellena `GROQ_API_KEY`.
2. Coloca los XML TEI de entrada en `outputs/xmls/`.
   - Deben terminar en `.tei.xml`.
   - Ejemplo: `outputs/xmls/paper01.tei.xml`.

Los XMLs son datos de entrada del pipeline. Si ya estan en el repo al clonarlo,
no hace falta copiarlos de nuevo.

## Ejecucion

Desde `containers/`:

```bash
docker compose up -d --build
```

Despues abre n8n en `http://localhost:5678`, importa manualmente el workflow
desde:

```text
containers/workflow/pipegrobid_workflow.json
```

Una vez importado, entra en `pipegrobid_workflow` y ejecutalo manualmente.

## Si faltan XMLs

El workflow fallara en `step_2` con un error indicando que no existen XMLs
`.tei.xml` en `outputs/xmls/`. En ese caso, copia los XMLs a esa carpeta y
vuelve a ejecutar el workflow.
