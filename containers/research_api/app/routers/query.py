from fastapi import APIRouter

from core.kg import execute_sparql_query
from schemas.fuseki import FusekiQueryRequest, FusekiQueryResponse


router = APIRouter(prefix="/query")


@router.post("", response_model=FusekiQueryResponse)
def send_query_to_fuseki(query_request: FusekiQueryRequest):
    """Endpoint avanzado para enviar SPARQL libre a Fuseki durante depuracion."""
    return execute_sparql_query(
        query=query_request.query,
        query_type=query_request.query_type,
    )
