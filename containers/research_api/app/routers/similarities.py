from fastapi import APIRouter, HTTPException, Path, Query

from queries.similarities import build_paper_similarities_query
from routers.common import id_from_uri, select_rows, to_float
from schemas.domain import PaperSimilarityItem


router = APIRouter(prefix="/similarities")


@router.get("/{paper_id}", response_model=list[PaperSimilarityItem])
def list_paper_similarities(
    paper_id: str = Path(
        description="Identificador del paper base: paper01, g4:paper01 o URI completa.",
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
        description="Numero maximo de papers similares a devolver.",
    ),
):
    """Papers similares a un paper concreto."""
    try:
        query = build_paper_similarities_query(
            paper_id=paper_id,
            limit=limit,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    rows = select_rows(query)
    similarities: list[PaperSimilarityItem] = []

    for row in rows:
        similarity_id = row.get("similarity_id")

        if not similarity_id:
            similarity_id = id_from_uri(row.get("similarity"))

        source_paper_id = row.get("source_paper_id")

        if not source_paper_id:
            source_paper_id = id_from_uri(row.get("sourcePaper"))

        target_paper_id = row.get("target_paper_id")

        if not target_paper_id:
            target_paper_id = id_from_uri(row.get("targetPaper"))

        similarity = PaperSimilarityItem(
            similarity_id=similarity_id,
            source_paper_id=source_paper_id,
            target_paper_id=target_paper_id,
            score=to_float(row.get("score")),
        )
        similarities.append(similarity)

    return similarities
