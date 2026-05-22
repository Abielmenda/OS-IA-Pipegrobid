import os


class Settings:
    FUSEKI_QUERY_URL: str = os.getenv(
        "FUSEKI_QUERY_URL",
        "http://localhost:3030/kg/query"
    )


settings = Settings()