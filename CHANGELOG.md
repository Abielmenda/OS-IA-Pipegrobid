
# Novedades

## Parseo de XMLs generados por grobid

- añadidos scripts para la extracción de información estructurada:

    - initial_parse.py:
        contiene funciones para el parseo de los datos estructurados del xml generado a partir
        del pdf con los que se puede nutrir el KG

        Actualmente permite extraer:

        - Información del paper:
            - título
            - abstract
            - fecha de publicación
            - identificador local
            - DOI pendiente de enriquecimiento externo

        - Información de autores:
            - nombre
            - orden de autoría
            - ORCID pendiente de enriquecimiento externo

        - Información de acknowledgements:
            - texto bruto de la sección
            - marcado como pendiente de extracción mediante LLM/NER

    - parse_grobid_xml.py:
        Contiene el flujo de parseo de los XML.

        Su función es:

        1. Recorrer los XML generados por GROBID.
        2. Aplicar las funciones de parseo definidas en `initial_parse.py`.
        3. Generar un JSON estructurado por cada paper.
        4. Guardar los resultados en la carpeta de salida correspondiente.
        

## NER y extracción de dichas entidades de los acknowledgements
- Realizado corpus (golden standar) y estudio sobre transformers y LLMs para obtener el mejor para nuestro proyecto (vencedor: LLM `llama-3.3-70b-versatile`)

- Uso de LLM ``llama-3.3-70b-versatile`` para reconocimiento de entidades en "acknowledgements". El objetivo es extraer:

    - personas mencionadas
    - organizaciones financiadoras
    - proyectos
    - identificadores de grants/awards
    - posibles relaciones entre proyectos y financiadores



## TOPIC MODELING  + PAPER SIMILARITIES
- Generación de TopicModeling mediante `BERTopic` y embeddings para nutrir el KG con topics, pertenencia paper-topic y similaridades entre papers.

## Generación de KG local
- Enriquecimiento de los jsons con fuentes externas:
    - **OpenAIRE**: proyectos de investigación, fechas y financiación.
    - **ORCID**: identificadores y afiliaciones públicas de autores.
    - **Wikidata**: información de organizaciones, países e identificadores externos.

- Creación del KG local en formato `.ttl` a partir de los datos extraídos del XML, entidades reconocidas mediante IA, topics y relaciones de similaridad.


## Workflow n8n
Integración del workflow con `n8n`, `python_runner`, `Fuseki` y `research_api` para automatizar la generación del KG a partir de los papers seleccionados.

## Creación app RESEARCH
Realizado backend y frontend de una aplicación usando `FASTAPI` y `Streamlit` que realiza consultas SPARQL al KG desplegado con ``fuseki`` visualizando los resultados de manera estructurada con el objetivo marcado en `/assigment_2/step_1`



