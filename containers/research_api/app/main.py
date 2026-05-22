from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import kg


app = FastAPI(
    title="Research Funding Knowledge Graph Analyzer API",
    description=(
        "Backend para consultar un Knowledge Graph RDF alojado en Apache Jena Fuseki."
    ),
    version="0.1.0"
)

# Preparado para conectar después con Streamlit u otro frontend.
origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(kg.router, prefix = "/kg",tags=["kg"])



@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


