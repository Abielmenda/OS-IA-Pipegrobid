from typing import Any

import requests
from fastapi import HTTPException

from core import kg as kg_client


def select_rows(query: str) -> list[dict[str, Any]]:
    """Obtiene filas desde core.kg y controla timeouts de Fuseki."""
    try:
        response = kg_client.execute_sparql_query(query=query, query_type="SELECT")
    except requests.exceptions.Timeout as error:
        raise HTTPException(status_code=504, detail="Fuseki query timeout.") from error

    results = response.get("results")

    if not isinstance(results, list):
        return []

    return results


def split_pipe_values(value: Any) -> list[str]:
    """Convierte GROUP_CONCAT separado por | en una lista sin duplicados."""
    if not value:
        return []

    values: list[str] = []
    seen_values = set()

    for raw_part in str(value).split("|"):
        part = raw_part.strip()

        if not part:
            continue

        if part in seen_values:
            continue

        seen_values.add(part)
        values.append(part)

    return values


def to_int(value: Any) -> int:
    """Convierte literales numericos de SPARQL a int."""
    if value in (None, ""):
        return 0

    return int(float(str(value)))


def to_float(value: Any) -> float:
    """Convierte literales numericos de SPARQL a float."""
    if value in (None, ""):
        return 0.0

    return float(str(value))


def to_optional_float(value: Any) -> float | None:
    """Convierte numericos opcionales sin confundir dato ausente con 0."""
    if value in (None, ""):
        return None

    return float(str(value))


def has_known_amount(row: dict[str, Any], count_key: str = "funding_amount_count") -> bool:
    """Indica si una agregacion incluia algun g4:fundingAmount real."""
    return to_int(row.get(count_key)) > 0


def id_from_uri(value: Any) -> str:
    """Extrae el identificador corto desde una URI RDF."""
    if not value:
        return ""

    text = str(value)
    after_hash = text.rsplit("#", 1)[-1]
    return after_hash.rsplit("/", 1)[-1]


