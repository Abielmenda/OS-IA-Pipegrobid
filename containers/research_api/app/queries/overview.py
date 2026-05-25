def build_summary_query() -> str:
    """Cuenta las entidades principales del KG para el panel de resumen."""
    return """
SELECT ?papers ?authors ?organizations ?projects ?countries ?topics ?paper_similarities
WHERE {
  # Cada contador va en una subquery independiente para evitar productos cartesianos.
  { SELECT (COUNT(DISTINCT ?paper) AS ?papers)
    WHERE { ?paper a g4:Paper . }
  }

  { SELECT (COUNT(DISTINCT ?author) AS ?authors)
    WHERE { ?author a foaf:Person . }
  }

  { SELECT (COUNT(DISTINCT ?organization) AS ?organizations)
    WHERE { ?organization a schema:Organization . }
  }

  { SELECT (COUNT(DISTINCT ?project) AS ?projects)
    WHERE { ?project a schema:Project . }
  }

  { SELECT (COUNT(DISTINCT ?country) AS ?countries)
    WHERE { ?country a schema:Country . }
  }

  { SELECT (COUNT(DISTINCT ?topic) AS ?topics)
    WHERE { ?topic a g4:Topic . }
  }

  { SELECT (COUNT(DISTINCT ?paperSimilarity) AS ?paper_similarities)
    WHERE { ?paperSimilarity a g4:PaperSimilarity . }
  }
}
""".strip()
