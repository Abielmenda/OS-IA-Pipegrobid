from fastapi import APIRouter

from queries.overview import build_summary_query
from routers.common import select_rows, to_int
from schemas.domain import SummaryResponse


router = APIRouter()


@router.get("/info")
def kg_info():
    """Endpoint descriptivo para comprobar que el backend del KG esta listo."""
    return {
        "name": "Research Funding Knowledge Graph",
        "description": "KG sobre papers, autores, organizaciones, proyectos, topics y similitudes.",
        "backend": "FastAPI",
        "kg_store": "Apache Jena Fuseki",
        "status": "ready",
    }


@router.get("/summary", response_model=SummaryResponse)
def kg_summary():
    """Devuelve conteos generales para pintar el resumen inicial de la app."""
    rows = select_rows(build_summary_query())
    row = rows[0] if rows else None

    if row is None:
        row = {}

    return SummaryResponse(
        papers=to_int(row.get("papers")),
        authors=to_int(row.get("authors")),
        organizations=to_int(row.get("organizations")),
        projects=to_int(row.get("projects")),
        countries=to_int(row.get("countries")),
        topics=to_int(row.get("topics")),
        paper_similarities=to_int(row.get("paper_similarities")),
    )
