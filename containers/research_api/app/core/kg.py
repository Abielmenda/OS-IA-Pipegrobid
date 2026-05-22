from typing import Any
import re

import requests

from core.config import settings


DEFAULT_PREFIXES = {
    "g4": "https://g4.org/ontology/research-funding#",
    "schema": "https://schema.org/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def add_default_prefixes(query: str) -> str:
    """
    Añade automáticamente los prefijos base del KG a la consulta SPARQL.

    Si la query ya tiene algún PREFIX definido, no lo duplica.
    """

    existing_prefixes = set(
        re.findall(r"PREFIX\s+([A-Za-z][\w-]*):", query, flags=re.IGNORECASE)
    )

    prefix_lines = []

    for prefix_name, prefix_uri in DEFAULT_PREFIXES.items():
        if prefix_name not in existing_prefixes:
            prefix_lines.append(f"PREFIX {prefix_name}: <{prefix_uri}>")

    return "\n".join(prefix_lines) + "\n\n" + query.strip()


def execute_sparql_query(query: str, query_type: str = "SELECT") -> dict[str, Any]:
    """
    Envía una consulta SPARQL a Fuseki y devuelve una respuesta normalizada.
    """

    query_type = query_type.upper()

    query = add_default_prefixes(query)

    if query_type in ["SELECT", "ASK"]:
        accept_header = "application/sparql-results+json"
    else:
        accept_header = "text/turtle"

    headers = {
        "Accept": accept_header
    }

    data = {
        "query": query
    }

    response = requests.post(
        settings.FUSEKI_QUERY_URL,
        data=data,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

    if "json" in content_type:
        raw_response = response.json()

        return {
            "query_type": query_type,
            "results": parse_sparql_json_results(raw_response, query_type),
            "raw_response": raw_response,
            "raw_text": None,
            "status_code": response.status_code
        }

    return {
        "query_type": query_type,
        "results": response.text,
        "raw_response": None,
        "raw_text": response.text,
        "status_code": response.status_code
    }


def parse_sparql_json_results(raw_response: dict[str, Any], query_type: str) -> Any:
    """
    Convierte la respuesta JSON de Fuseki en una estructura más cómoda para la API.
    """

    if query_type == "ASK":
        return raw_response.get("boolean")

    bindings = raw_response.get("results", {}).get("bindings", [])

    parsed_results = []

    for row in bindings:
        parsed_row = {}

        for variable_name, variable_data in row.items():
            parsed_row[variable_name] = variable_data.get("value")

        parsed_results.append(parsed_row)

    return parsed_results