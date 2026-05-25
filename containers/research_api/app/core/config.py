import os


class Settings:
    FUSEKI_QUERY_URL: str = os.getenv(
        "FUSEKI_QUERY_URL",
        "http://localhost:3030/kg/query"
    )
    FUSEKI_TIMEOUT_SECONDS: int = int(os.getenv("FUSEKI_TIMEOUT_SECONDS", "30"))


settings = Settings()
