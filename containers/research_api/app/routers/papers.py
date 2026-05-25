from fastapi import APIRouter, HTTPException, Path, Query

from queries.papers import build_paper_detail_query, build_papers_query
from routers.common import (
    id_from_uri,
    select_rows,
    split_pipe_values,
)
from schemas.domain import PaperDetail, PaperListItem, PersonInfo


router = APIRouter(prefix="/papers")


def empty_to_none(value: str) -> str | None:
    """Evita mostrar campos vacios como cadenas vacias en la ficha."""
    value = value.strip()

    if not value:
        return None

    return value


def person_info_from_pipe_values(value: str | None) -> list[PersonInfo]:
    """Convierte filas compactas de SPARQL en fichas de persona."""
    people: list[PersonInfo] = []
    seen_people = set()

    for raw_person in split_pipe_values(value):
        parts = raw_person.split("~")

        while len(parts) < 5:
            parts.append("")

        name = parts[0].strip()

        if not name:
            continue

        person_id = empty_to_none(parts[3])
        unique_key = person_id or name

        if unique_key in seen_people:
            continue

        seen_people.add(unique_key)

        people.append(
            PersonInfo(
                name=name,
                orcid=empty_to_none(parts[1]),
                affiliation=empty_to_none(parts[2]),
                person_id=person_id,
                uri=empty_to_none(parts[4]),
            )
        )

    return people


def paper_from_row(row: dict) -> PaperListItem:
    """Mapea una fila agregada de SPARQL al schema de paper."""
    paper_id = row.get("paper_id") or id_from_uri(row.get("paper"))

    return PaperListItem(
        paper_id=paper_id,
        uri=row.get("uri") or row.get("paper"),
        title=row.get("title"),
        date=row.get("date"),
        authors=split_pipe_values(row.get("authors")),
        projects=split_pipe_values(row.get("projects")),
        funders=split_pipe_values(row.get("funders")),
        countries=split_pipe_values(row.get("countries")),
        topics=split_pipe_values(row.get("topics")),
    )


@router.get("", response_model=list[PaperListItem])
def list_papers(
    search: str | None = Query(
        default=None,
        description="Texto a buscar en el titulo o abstract del paper.",
    ),
    topic_id: int | None = Query(
        default=None,
        description="Identificador numerico del topic generado en el KG, por ejemplo 0.",
    ),
    country: str | None = Query(
        default=None,
        description="Filtra papers por pais del organismo financiador.",
    ),
    organization: str | None = Query(
        default=None,
        description="Filtra papers por nombre del organismo financiador.",
    ),
    project: str | None = Query(
        default=None,
        description="Filtra papers por nombre o identificador del proyecto/grant.",
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
        description="Numero maximo de resultados a devolver.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Numero de resultados a saltar para paginacion.",
    ),
):
    """Listado principal de papers con filtros de busqueda y financiacion."""
    query = build_papers_query(
        search=search,
        topic_id=topic_id,
        country=country,
        organization=organization,
        project=project,
        limit=limit,
        offset=offset,
    )
    rows = select_rows(query)

    papers: list[PaperListItem] = []

    for row in rows:
        paper = paper_from_row(row)
        papers.append(paper)

    return papers


@router.get("/{paper_id}", response_model=PaperDetail)
def paper_detail(
    paper_id: str = Path(
        description="Identificador del paper: paper01, g4:paper01 o URI completa.",
    ),
):
    """Ficha de un paper: metadatos, financiacion, topics y similitudes."""
    try:
        query = build_paper_detail_query(paper_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    rows = select_rows(query)
    row = rows[0] if rows else None

    if row is None:
        raise HTTPException(status_code=404, detail="Paper not found")

    paper = paper_from_row(row)

    return PaperDetail(
        paper_id=paper.paper_id,
        uri=paper.uri,
        title=paper.title,
        date=paper.date,
        abstract=row.get("abstract"),
        authors=paper.authors,
        projects=paper.projects,
        funders=paper.funders,
        countries=paper.countries,
        topics=paper.topics,
        acknowledged_organizations=split_pipe_values(row.get("acknowledged_organizations")),
        acknowledged_people=split_pipe_values(row.get("acknowledged_people")),
        authors_info=person_info_from_pipe_values(row.get("authors_info")),
        acknowledged_people_info=person_info_from_pipe_values(
            row.get("acknowledged_people_info")
        ),
    )
