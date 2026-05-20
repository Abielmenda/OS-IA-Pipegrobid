# README PROVISIONAL — Online Enrichment

> Este README es provisional para que los compañeros entiendan qué hace este módulo y puedan validarlo.

---

## ¿Qué hace este módulo?

Coge los JSONs que genera `enrich_jsons.py` del topic_modeling (que ya tienen topics y similarities) y los enriquece con datos de tres fuentes externas:

- **OpenAIRE** → datos de proyectos (título, fechas, dinero financiado)
- **Wikidata** → datos de organizaciones (descripción, país)
- **ORCID** → datos de personas (identificador único, afiliación)

Los JSONs de entrada están en `outputs/topics/enriched_jsons/` y los resultados se guardan en `outputs/topics/kg_enriched/` (carpeta nueva, no sobreescribe nada).

---

## Flujo

```
enrich_jsons.py  →  enriched_jsons/  →  enrich_online.py  →  kg_enriched/  →  local_kg.py
```

---

## Cómo funciona cada script

### openaire.py

Hace una petición HTTP a la API de OpenAIRE con el código del proyecto:
```
https://api.openaire.eu/search/projects?grantID=851173&format=json
```
OpenAIRE devuelve un JSON del que extraemos título, fechas y cantidad financiada.

Si no encuentra el proyecto devuelve `None` y ese proyecto se queda sin enriquecer. Esto pasa principalmente con proyectos no europeos.

**Validación**: probado con el proyecto `851173` del paper_13 → devuelve correctamente título, fechas 2020-2026 y 1.498.210 EUR.

---

### wikidata.py

Consulta Wikidata usando **SPARQL** (el lenguaje de consulta estándar para bases de datos de grafos). Busca la organización por su nombre en inglés y obtiene su país usando la propiedad `P17` (que en Wikidata significa "país").

Wikidata exige identificarse con un `User-Agent` en la cabecera de la petición o devuelve error 403.

**Validación**: probado con `"European Research Council"` → devuelve identificador `Q1377836` y país `Belgium`.

---

### orcid.py

Busca una persona en ORCID en **dos pasos**:

1. Busca por nombre y apellido → obtiene el ORCID ID
2. Con ese ID pide el perfil completo → obtiene la afiliación

Necesitamos dos llamadas porque la búsqueda solo devuelve el ID, no el perfil completo.

ORCID necesita la cabecera `Accept: application/json` o devuelve XML en vez de JSON.

Solo funciona con nombres completos. Las iniciales (`S.G.`, `CJP`) o pseudónimos (`xlr8harder`) no se pueden buscar.

**Validación**: probado con `"Anne-Florence Bitbol"` del paper_13 → devuelve ORCID `0000-0003-1020-494X` y afiliación `École Polytechnique Fédérale de Lausanne`.

---

### enrich_online.py

Es el script principal. Lee cada JSON de `enriched_jsons/`, llama a los tres scripts anteriores y guarda el resultado en `kg_enriched/`.

Hay dos cosas importantes que hace antes de llamar a las APIs:

**1. Limpiar identificadores de proyectos**

El LLM a veces devuelve los códigos con texto de más, por ejemplo `"grant agreement No. 851173"`. Usamos patrones (regex) para extraer solo el código real. Un patrón es una expresión que describe la forma de un texto. Por ejemplo `\b\d{5,}\b` significa "busca 5 o más dígitos seguidos" y extrae `851173` de ese texto sucio.

Los nombres de programas como `"Horizon 2020"` no encajan en ningún patrón y se descartan porque no son códigos reales de proyectos.

**2. Limpiar nombres de organizaciones**

Wikidata tiene registrado el nombre completo sin acrónimo. Por eso quitamos el acrónimo entre paréntesis antes de buscar:
`"European Research Council (ERC)"` → `"European Research Council"`

---

## Replicación

```bash
# Paso 1: generar los JSONs de entrada (si no existen ya)
cd assigment_2/step_3/topic_modeling
poetry run python scripts/enrich_jsons.py

# Paso 2: ejecutar el enriquecimiento online
cd assigment_2/step_3/online_enrichment/scripts
python3 enrich_online.py
```

---

## Limitaciones conocidas

- **OpenAIRE** no tiene proyectos de agencias no europeas (ej: NSF americana, Czech Science Foundation). Esos proyectos quedan sin enriquecer.
- **ORCID** no permite buscar por iniciales ni pseudónimos. Esas personas quedan sin identificador.
- **Wikidata** devuelve `"Internationality"` para organizaciones supranacionales como la UE. Esos casos quedan sin país en el grafo.
- Algunas personas tienen el perfil de ORCID desactualizado y su afiliación queda como `null`.

