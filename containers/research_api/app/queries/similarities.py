from queries.common import normalize_paper_id, result_window_clause


def build_paper_similarities_query(
    paper_id: str,
    limit: int = 50,
) -> str:
    """Lista los papers similares a un paper concreto."""
    normalized_paper_id = normalize_paper_id(paper_id)

    return f"""
SELECT ?similarity ?similarity_id ?source_paper_id ?targetPaper ?target_paper_id ?score
WHERE {{
  # El endpoint recibe paper01, g4:paper01 o URI; aqui ya esta normalizado.
  BIND(g4:{normalized_paper_id} AS ?paper)
  BIND("{normalized_paper_id}" AS ?source_paper_id)

  # La similitud es bidireccional: el paper puede estar en paper1 o paper2.
  {{
    ?similarity a g4:PaperSimilarity ;
                g4:paper1 ?paper ;
                g4:paper2 ?targetPaper ;
                g4:score ?score .
  }} UNION {{
    ?similarity a g4:PaperSimilarity ;
                g4:paper1 ?targetPaper ;
                g4:paper2 ?paper ;
                g4:score ?score .
  }}

  # IDs cortos para que la app no dependa de URIs completas.
  BIND(REPLACE(STR(?similarity), "^.*[#/]", "") AS ?similarity_id)
  BIND(REPLACE(STR(?targetPaper), "^.*[#/]", "") AS ?target_paper_id)
}}
ORDER BY DESC(?score)
{result_window_clause(limit)}
""".strip()
