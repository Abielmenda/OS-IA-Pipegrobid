import os
from typing import Any

import requests


DEFAULT_API_URL = "http://localhost:8000"
DEFAULT_TIMEOUT = 15


class ApiClientError(RuntimeError):
    """Error legible para mostrar problemas de API en Streamlit."""


def build_query_params(**values: Any) -> dict[str, Any]:
    """Devuelve solo parametros activos para evitar filtros vacios en la API."""
    params: dict[str, Any] = {}

    for key, value in values.items():
        if value is None:
            continue

        if value == "":
            continue

        params[key] = value

    return params


class ApiClient:
    """Cliente HTTP pequeno para consumir `research_api` desde Streamlit."""

    def __init__(
        self,
        base_url: str | None = None,
        session: requests.Session | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        configured_url = base_url or os.getenv("RESEARCH_API_URL", DEFAULT_API_URL)
        self.base_url = configured_url.rstrip("/")
        self.session = session or requests.Session()
        self.timeout = timeout

    def _url(self, path: str) -> str:
        clean_path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{clean_path}"

    def _parse_response(self, response: requests.Response) -> Any:
        try:
            payload = response.json()
        except ValueError:
            payload = response.text

        if response.status_code >= 400:
            detail = payload

            if isinstance(payload, dict):
                detail = payload.get("detail") or payload

            raise ApiClientError(f"API error {response.status_code}: {detail}")

        return payload

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = self.session.get(
            self._url(path),
            params=params,
            timeout=self.timeout,
        )
        return self._parse_response(response)

    def post(self, path: str, payload: dict[str, Any]) -> Any:
        response = self.session.post(
            self._url(path),
            json=payload,
            timeout=self.timeout,
        )
        return self._parse_response(response)

    def get_health(self) -> dict[str, Any]:
        return self.get("/health")

    def get_kg_info(self) -> dict[str, Any]:
        return self.get("/kg/info")

    def get_summary(self) -> dict[str, Any]:
        return self.get("/kg/summary")

    def get_funding_countries(
        self,
        topic_id: int | str | None = None,
    ) -> list[dict[str, Any]]:
        params = build_query_params(topic_id=topic_id)
        return self.get("/kg/funding/countries", params=params)

    def get_funding_topics(self) -> list[dict[str, Any]]:
        return self.get("/kg/funding/topics")

    def get_funding_organizations(
        self,
        limit: int = 50,
        topic_id: int | str | None = None,
    ) -> list[dict[str, Any]]:
        params = build_query_params(limit=limit, topic_id=topic_id)
        return self.get("/kg/funding/organizations", params=params)

    def get_papers(
        self,
        search: str | None = None,
        topic_id: int | str | None = None,
        country: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        params = build_query_params(
            search=search,
            topic_id=topic_id,
            country=country,
            organization=organization,
            project=project,
            limit=limit,
            offset=offset,
        )
        return self.get("/kg/papers", params=params)

    def get_paper_detail(self, paper_id: str) -> dict[str, Any]:
        return self.get(f"/kg/papers/{paper_id}")

    def get_projects(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        params = build_query_params(limit=limit, offset=offset)
        return self.get("/kg/projects", params=params)

    def get_topics(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        params = build_query_params(limit=limit, offset=offset)
        return self.get("/kg/topics", params=params)

    def get_similarities(
        self,
        paper_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        params = build_query_params(limit=limit)
        return self.get(f"/kg/similarities/{paper_id}", params=params)

    def run_sparql_query(
        self,
        query: str,
        query_type: str = "SELECT",
    ) -> dict[str, Any]:
        payload = {
            "query": query,
            "query_type": query_type,
        }
        return self.post("/kg/query", payload)
