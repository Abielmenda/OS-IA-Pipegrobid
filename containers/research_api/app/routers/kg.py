from fastapi import APIRouter, HTTPException

from core.kg import execute_sparql_query
from schemas.fuseki import FusekiQueryRequest, FusekiQueryResponse
import requests


router = APIRouter()





@router.get("/info")
def kg_info():
    """
    Devuelve información básica sobre el Knowledge Graph.
    """

    return {
        "name": "Research Funding Knowledge Graph",
        "description": "KG sobre papers, autores, organizaciones, proyectos, topics y similitudes.",
        "backend": "FastAPI",
        "kg_store": "Apache Jena Fuseki",
        "status": "ready"
    }


@router.post("/query", response_model=FusekiQueryResponse)
def send_query_to_fuseki(query_request: FusekiQueryRequest):
    """
    Recibe una consulta SPARQL y la envía a Fuseki.
    """

    try:
        return execute_sparql_query(
            query=query_request.query,
            query_type=query_request.query_type
        )

    except requests.exceptions.HTTPError as error:
        raise HTTPException(
            status_code=502,
            detail=f"Fuseki returned an HTTP error: {str(error)}"
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Fuseki. Check that Fuseki is running."
        )

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Fuseki query timeout."
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while querying Fuseki: {str(error)}"
        )