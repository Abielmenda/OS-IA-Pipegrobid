from typing import Any, Literal

from pydantic import BaseModel, Field


class FusekiQueryRequest(BaseModel):
    query: str = Field(
        description="Consulta SPARQL que se enviará a Fuseki."
    )

    query_type: Literal["SELECT", "ASK", "CONSTRUCT", "DESCRIBE"] = Field(
        default="SELECT",
        description="Tipo de consulta SPARQL."
    )


class FusekiQueryResponse(BaseModel):
    query_type: str
    results: Any | None = None
    raw_response: dict[str, Any] | None = None
    raw_text: str | None = None
    status_code: int