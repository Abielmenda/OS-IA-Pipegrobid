from __future__ import annotations

import re

from core.kg import DEFAULT_PREFIXES

# Namespace base del KG generado. Se reutiliza el prefijo declarado en core/kg.py
# para no mantener la misma URI en dos sitios.
G4_BASE = DEFAULT_PREFIXES["g4"]


def normalize_paper_id(value: str) -> str:
    """Normaliza ids de paper recibidos desde la API antes de usarlos en SPARQL."""
    paper_id = value.strip()

    if paper_id.startswith(G4_BASE):
        paper_id = paper_id.removeprefix(G4_BASE)

    if paper_id.startswith("g4:"):
        paper_id = paper_id.removeprefix("g4:")

    if not re.fullmatch(r"paper\d+", paper_id):
        raise ValueError("paper_id must look like paper01")

    return paper_id


def literal_filter_value(value: str) -> str:
    """Escapa texto libre usado dentro de FILTER para evitar romper la query."""
    escaped = value.replace("\\", "\\\\")
    escaped = escaped.replace('"', '\\"')
    return escaped.lower()


def result_window_clause(
    limit: int,
    offset: int | None = None,
    max_limit: int = 200,
) -> str:
    """Construye LIMIT/OFFSET para las queries que devuelven listados."""
    safe_limit = max(1, min(limit, max_limit))

    if offset is None:
        return f"LIMIT {safe_limit}"

    safe_offset = max(0, offset)
    return f"LIMIT {safe_limit}\nOFFSET {safe_offset}"
