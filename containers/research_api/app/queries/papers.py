from __future__ import annotations

from queries.common import literal_filter_value, normalize_paper_id, result_window_clause


def build_papers_query(
    search: str | None = None,
    topic_id: int | None = None,
    country: str | None = None,
    organization: str | None = None,
    project: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> str:
    """Lista papers con filtros pensados para la pantalla principal de busqueda."""
    base_patterns = [
        "# Recurso principal: cada fila agregada representa un paper.",
        "?paper a g4:Paper .",
        'BIND(REPLACE(STR(?paper), "^.*[#/]", "") AS ?paper_id)',
        "",
        "# Metadatos basicos usados para mostrar y filtrar antes de paginar.",
        "OPTIONAL { ?paper dc:title ?title . }",
        "OPTIONAL { ?paper dc:date ?date . }",
        "OPTIONAL { ?paper schema:abstract ?abstract . }",
    ]
    filters = []

    if search:
        search_value = literal_filter_value(search)
        filters.append(
            f'FILTER(CONTAINS(LCASE(?title), "{search_value}") || '
            f'CONTAINS(LCASE(?abstract), "{search_value}"))'
        )

    if topic_id is not None:
        base_patterns.append("# Filtro exacto por topic generado en el KG.")
        base_patterns.append(
            "?paperTopicFilter g4:paper ?paper ; "
            f"g4:topic g4:topic_{topic_id} ."
        )

    if country:
        country_value = literal_filter_value(country)
        filters.append(
            """
FILTER EXISTS {
  ?paper g4:fundedByProject ?countryProject .
  ?countryProject schema:funder ?countryOrg .
  ?countryOrg schema:location ?countryNode .
  ?countryNode schema:name ?countryName .
  FILTER(CONTAINS(LCASE(?countryName), "%s"))
}
""".strip()
            % country_value
        )

    if organization:
        organization_value = literal_filter_value(organization)
        filters.append(
            """
FILTER EXISTS {
  ?paper g4:fundedByProject ?orgProject .
  ?orgProject schema:funder ?orgNode .
  ?orgNode schema:name ?orgName .
  FILTER(CONTAINS(LCASE(?orgName), "%s"))
}
""".strip()
            % organization_value
        )

    if project:
        project_value = literal_filter_value(project)
        filters.append(
            """
FILTER EXISTS {
  ?paper g4:fundedByProject ?projectNode .
  OPTIONAL { ?projectNode schema:name ?projectName . }
  OPTIONAL { ?projectNode schema:identifier ?projectIdentifier . }
  FILTER(
    (BOUND(?projectName) && CONTAINS(LCASE(?projectName), "%s")) ||
    (BOUND(?projectIdentifier) && CONTAINS(LCASE(?projectIdentifier), "%s"))
  )
}
""".strip()
            % (project_value, project_value)
        )

    base_where_lines = base_patterns + filters
    base_where_block = "\n    ".join(base_where_lines)

    return f"""
SELECT ?paper ?paper_id ?title ?date ?authors ?projects ?funders ?countries ?topics
WHERE {{
  # Primero se pagina el conjunto de papers. Asi las agregaciones no multiplican
  # autores x proyectos x funders x paises x topics en una unica tabla temporal.
  {{
    SELECT ?paper ?paper_id ?title ?date
    WHERE {{
      {base_where_block}
    }}
    ORDER BY ?paper_id
    {result_window_clause(limit, offset)}
  }}

  # Autores agregados por paper.
  OPTIONAL {{
    SELECT ?paper (GROUP_CONCAT(DISTINCT ?authorName; separator="|") AS ?authors)
    WHERE {{
      ?paper schema:author ?author .
      ?author schema:name ?authorName .
    }}
    GROUP BY ?paper
  }}

  # Proyectos agregados por paper.
  OPTIONAL {{
    SELECT ?paper (GROUP_CONCAT(DISTINCT ?projectName; separator="|") AS ?projects)
    WHERE {{
      ?paper g4:fundedByProject ?projectNode .
      ?projectNode schema:name ?projectName .
    }}
    GROUP BY ?paper
  }}

  # Organismos financiadores agregados por paper.
  OPTIONAL {{
    SELECT ?paper (GROUP_CONCAT(DISTINCT ?orgName; separator="|") AS ?funders)
    WHERE {{
      ?paper g4:fundedByProject ?projectNode .
      ?projectNode schema:funder ?org .
      ?org schema:name ?orgName .
    }}
    GROUP BY ?paper
  }}

  # Paises agregados por paper desde la cadena paper -> proyecto -> funder -> pais.
  OPTIONAL {{
    SELECT ?paper (GROUP_CONCAT(DISTINCT ?countryName; separator="|") AS ?countries)
    WHERE {{
      ?paper g4:fundedByProject ?projectNode .
      ?projectNode schema:funder ?org .
      ?org schema:location ?countryNode .
      ?countryNode schema:name ?countryName .
    }}
    GROUP BY ?paper
  }}

  # Topics agregados por paper.
  OPTIONAL {{
    SELECT ?paper (GROUP_CONCAT(DISTINCT ?topicName; separator="|") AS ?topics)
    WHERE {{
      ?paperTopic g4:paper ?paper ; g4:topic ?topic .
      ?topic schema:name ?topicName .
    }}
    GROUP BY ?paper
  }}
}}
ORDER BY ?paper_id
""".strip()


def build_paper_detail_query(paper_id: str) -> str:
    """Obtiene una ficha completa de un paper concreto."""
    normalized_paper_id = normalize_paper_id(paper_id)

    return f"""
SELECT ?paper ?paper_id ?title ?date ?abstract
       (GROUP_CONCAT(DISTINCT ?authorName; separator="|") AS ?authors)
       (GROUP_CONCAT(DISTINCT ?authorInfo; separator="|") AS ?authors_info)
       (GROUP_CONCAT(DISTINCT ?projectName; separator="|") AS ?projects)
       (GROUP_CONCAT(DISTINCT ?funderName; separator="|") AS ?funders)
       (GROUP_CONCAT(DISTINCT ?countryName; separator="|") AS ?countries)
       (GROUP_CONCAT(DISTINCT ?topicName; separator="|") AS ?topics)
       (GROUP_CONCAT(DISTINCT ?acknowledgedOrganizationName; separator="|") AS ?acknowledged_organizations)
       (GROUP_CONCAT(DISTINCT ?acknowledgedPersonName; separator="|") AS ?acknowledged_people)
       (GROUP_CONCAT(DISTINCT ?acknowledgedPersonInfo; separator="|") AS ?acknowledged_people_info)
WHERE {{
  # El endpoint recibe paper01, g4:paper01 o URI; aqui ya esta normalizado.
  BIND(g4:{normalized_paper_id} AS ?paper)
  BIND("{normalized_paper_id}" AS ?paper_id)
  ?paper a g4:Paper .

  # Datos descriptivos del paper.
  OPTIONAL {{ ?paper dc:title ?title . }}
  OPTIONAL {{ ?paper dc:date ?date . }}
  OPTIONAL {{ ?paper schema:abstract ?abstract . }}
  OPTIONAL {{
    ?paper schema:author ?author .
    ?author schema:name ?authorName .
    OPTIONAL {{ ?author schema:identifier ?authorOrcid . }}
    OPTIONAL {{
      ?author schema:affiliation ?authorAffiliation .
      ?authorAffiliation schema:name ?authorAffiliationName .
    }}
    BIND(REPLACE(STR(?author), "^.*[#/]", "") AS ?authorId)
    BIND(
      CONCAT(
        STR(?authorName),
        "~",
        COALESCE(STR(?authorOrcid), ""),
        "~",
        COALESCE(STR(?authorAffiliationName), ""),
        "~",
        ?authorId,
        "~",
        STR(?author)
      ) AS ?authorInfo
    )
  }}

  # Cadena paper -> proyecto -> financiador -> pais.
  OPTIONAL {{
    ?paper g4:fundedByProject ?project .
    ?project schema:name ?projectName .
    OPTIONAL {{
      ?project schema:funder ?funder .
      ?funder schema:name ?funderName .
      OPTIONAL {{
        ?funder schema:location ?country .
        ?country schema:name ?countryName .
      }}
    }}
  }}

  # Topics asignados por el pipeline de KG.
  OPTIONAL {{
    ?paperTopic g4:paper ?paper ; g4:topic ?topic .
    ?topic schema:name ?topicName .
  }}

  # Entidades reconocidas en acknowledgements, separadas por tipo RDF.
  OPTIONAL {{
    ?paper g4:acknowledges ?acknowledgedOrganization .
    ?acknowledgedOrganization a schema:Organization ;
      schema:name ?acknowledgedOrganizationName .
  }}
  OPTIONAL {{
    ?paper g4:acknowledges ?acknowledgedPerson .
    ?acknowledgedPerson a foaf:Person ;
      schema:name ?acknowledgedPersonName .
    OPTIONAL {{ ?acknowledgedPerson schema:identifier ?acknowledgedPersonOrcid . }}
    OPTIONAL {{
      ?acknowledgedPerson schema:affiliation ?acknowledgedPersonAffiliation .
      ?acknowledgedPersonAffiliation schema:name ?acknowledgedPersonAffiliationName .
    }}
    BIND(REPLACE(STR(?acknowledgedPerson), "^.*[#/]", "") AS ?acknowledgedPersonId)
    BIND(
      CONCAT(
        STR(?acknowledgedPersonName),
        "~",
        COALESCE(STR(?acknowledgedPersonOrcid), ""),
        "~",
        COALESCE(STR(?acknowledgedPersonAffiliationName), ""),
        "~",
        ?acknowledgedPersonId,
        "~",
        STR(?acknowledgedPerson)
      ) AS ?acknowledgedPersonInfo
    )
  }}
}}
GROUP BY ?paper ?paper_id ?title ?date ?abstract
""".strip()
