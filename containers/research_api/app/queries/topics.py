from queries.common import result_window_clause


def build_topics_query(limit: int = 50, offset: int = 0) -> str:
    """Devuelve topics, keywords y papers representativos."""
    return f"""
SELECT ?topic ?topic_id ?name ?keywords
       (COUNT(DISTINCT ?paper) AS ?papers_count)
       (GROUP_CONCAT(DISTINCT ?paperId; separator="|") AS ?papers)
WHERE {{
  # Topic generado por el pipeline de analisis del KG.
  ?topic a g4:Topic .
  BIND(REPLACE(STR(?topic), "^.*topic_", "") AS ?topic_id)

  # Nombre y keywords ayudan al frontend a explicar cada cluster tematico.
  OPTIONAL {{ ?topic schema:name ?name . }}
  OPTIONAL {{ ?topic schema:keywords ?keywords . }}

  # Papers vinculados a cada topic.
  OPTIONAL {{
    ?paperTopic g4:topic ?topic ; g4:paper ?paper .
    BIND(REPLACE(STR(?paper), "^.*[#/]", "") AS ?paperId)
  }}
}}
GROUP BY ?topic ?topic_id ?name ?keywords
ORDER BY ?topic_id
{result_window_clause(limit, offset)}
""".strip()
