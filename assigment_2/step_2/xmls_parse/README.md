# Parseo de xmls generado por grobid
## Introducción
Este es el primer paso a llevar a cabo. Consiste en la extracción de la información estructurada de los xmls dejándo la extracción en formato json en `/assigment_2/step_2/outputs/parsed_xmls`.



## Explicación

A partir de bibliotecas relacionadas con xmls se pueden recorrer los nodos de dichos archivos. Desde ellos, podemos extraer información que nos es relevante para la generación de nuestro grafo de conocimiento. sobre:
1. El paper:
    - título (nodo <title>)
    - fecha de publicación (nodo <date type="published">)
    - abstract(entre el nodo <abstract>)
    - keywords(entre el nodo <keywords>)

2. Autores del paper:
    - nombre


## Replicación de la extracción
Primero debes haber ejecutado el pipegrobid para generar los xmls (desde `/` ejecutar `docker compose up -d`)


Posteriormente, desde el directorio `/assigment_2/step_2/xmls_parse` instalar el entorno poetry con `poetry install --no-root ` y ejecutar el mandato `poetry run python ./parse_grobid_xml.py` para obtener los jsons nutridos.

## Declaración de uso de IA
Se usó IA generativa para:
-  Encontrar los nodos del xml que contuvieran la información relevante que investigamos que podíamos encontrar en el xml
- Generar y entender el código de initial_parse.py bajo la guía supervisada de los autores, verificando que cada función funcionaba exactamente de la manera requerida.