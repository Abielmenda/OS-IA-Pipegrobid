import pytest

from api_client import ApiClient, ApiClientError, build_query_params


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload
        self.text = text

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append(("GET", url, params, timeout))
        return self.response

    def post(self, url, json=None, timeout=None):
        self.calls.append(("POST", url, json, timeout))
        return self.response


def test_build_query_params_removes_empty_values():
    params = build_query_params(
        search="machine learning",
        country="Spain",
        topic_id=None,
        organization="",
        limit=50,
        offset=0,
    )

    assert params == {
        "search": "machine learning",
        "country": "Spain",
        "limit": 50,
        "offset": 0,
    }


def test_get_papers_sends_only_active_filters():
    session = FakeSession(FakeResponse(payload=[]))
    client = ApiClient(base_url="http://api.test", session=session)

    result = client.get_papers(search="cancer", topic_id=2, country=None)

    assert result == []
    assert session.calls == [
        (
            "GET",
            "http://api.test/kg/papers",
            {"search": "cancer", "topic_id": 2, "limit": 50, "offset": 0},
            15,
        )
    ]


def test_get_funding_countries_accepts_topic_filter():
    session = FakeSession(FakeResponse(payload=[]))
    client = ApiClient(base_url="http://api.test", session=session)

    result = client.get_funding_countries(topic_id=1)

    assert result == []
    assert session.calls == [
        (
            "GET",
            "http://api.test/kg/funding/countries",
            {"topic_id": 1},
            15,
        )
    ]


def test_get_funding_organizations_accepts_topic_filter():
    session = FakeSession(FakeResponse(payload=[]))
    client = ApiClient(base_url="http://api.test", session=session)

    result = client.get_funding_organizations(limit=10, topic_id=1)

    assert result == []
    assert session.calls == [
        (
            "GET",
            "http://api.test/kg/funding/organizations",
            {"limit": 10, "topic_id": 1},
            15,
        )
    ]


def test_get_paper_detail_uses_paper_endpoint():
    session = FakeSession(FakeResponse(payload={"paper_id": "paper01"}))
    client = ApiClient(base_url="http://api.test/", session=session)

    result = client.get_paper_detail("paper01")

    assert result == {"paper_id": "paper01"}
    assert session.calls[0][1] == "http://api.test/kg/papers/paper01"


def test_run_sparql_query_posts_query_payload():
    session = FakeSession(FakeResponse(payload={"ok": True}))
    client = ApiClient(base_url="http://api.test", session=session)

    result = client.run_sparql_query("SELECT * WHERE { ?s ?p ?o }")

    assert result == {"ok": True}
    assert session.calls == [
        (
            "POST",
            "http://api.test/kg/query",
            {"query": "SELECT * WHERE { ?s ?p ?o }", "query_type": "SELECT"},
            15,
        )
    ]


def test_http_error_becomes_api_client_error():
    session = FakeSession(FakeResponse(status_code=504, payload={"detail": "Fuseki timeout"}))
    client = ApiClient(base_url="http://api.test", session=session)

    with pytest.raises(ApiClientError) as error:
        client.get_summary()

    assert "504" in str(error.value)
    assert "Fuseki timeout" in str(error.value)
