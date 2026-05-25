from fastapi import APIRouter, Query

from queries.topics import build_topics_query
from routers.common import id_from_uri, select_rows, split_pipe_values, to_int
from schemas.domain import TopicItem


router = APIRouter(prefix="/topics")


@router.get("", response_model=list[TopicItem])
def list_topics(
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
        description="Numero maximo de topics a devolver.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Numero de topics a saltar para paginacion.",
    ),
):
    """Topics del KG con keywords y papers asociados."""
    rows = select_rows(build_topics_query(limit=limit, offset=offset))
    topics: list[TopicItem] = []

    for row in rows:
        topic_id = row.get("topic_id") or id_from_uri(row.get("topic"))
        topic = TopicItem(
            topic_id=topic_id,
            name=row.get("name"),
            keywords=row.get("keywords"),
            papers_count=to_int(row.get("papers_count")),
            papers=split_pipe_values(row.get("papers")),
        )
        topics.append(topic)

    return topics
