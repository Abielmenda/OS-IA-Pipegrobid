from fastapi import APIRouter

from routers import funding, overview, papers, projects, query, similarities, topics


router = APIRouter()

# Este archivo solo agrega routers tematicos. `main.py` mantiene el prefijo /kg,
# por eso las URLs publicas no cambian aunque el codigo este separado.
router.include_router(overview.router, tags=["kg-overview"])
router.include_router(papers.router, tags=["kg-papers"])
router.include_router(funding.router, tags=["kg-funding"])
router.include_router(projects.router, tags=["kg-projects"])
router.include_router(topics.router, tags=["kg-topics"])
router.include_router(similarities.router, tags=["kg-similarities"])
router.include_router(query.router, tags=["kg-query"])
