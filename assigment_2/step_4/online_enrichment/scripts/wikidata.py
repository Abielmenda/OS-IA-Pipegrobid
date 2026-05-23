import requests

# Wikidata exige identificarse con un User-Agent o devuelve error 403
HEADERS = {"User-Agent": "G4_OPENSCIENCE/1.0 (proyecto universitario UPM)"}
SPARQL_URL = "https://query.wikidata.org/sparql"

def enrich_organization(nombre):
    # Consultamos Wikidata usando SPARQL buscando la organización por su nombre en inglés.
    # La propiedad P17 en Wikidata significa "país".
    # Si la organización no tiene país (por ejemplo, Unión Europea) el campo queda vacío.
    query = f"""
    SELECT ?org ?orgDescription ?country ?countryLabel WHERE {{
      ?org rdfs:label "{nombre}"@en .
      OPTIONAL {{ ?org wdt:P17 ?country . }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
    }}
    LIMIT 1
    """

    respuesta = requests.get(
        SPARQL_URL,
        params={"query": query, "format": "json"},
        headers=HEADERS
    )

    if respuesta.status_code != 200:
        return None

    datos = respuesta.json()
    resultados = datos["results"]["bindings"]

    if not resultados:
        return None

    fila = resultados[0]

    # El ID de Wikidata viene como URL completa, nos quedamos solo con el código.
    # Ejemplo: "http://www.wikidata.org/entity/Q1377836" -> "Q1377836"
    org_id = fila["org"]["value"].split("/")[-1]

    country_id = None
    country_name = None
    if "country" in fila:
        country_id = fila["country"]["value"].split("/")[-1]
        country_name = fila.get("countryLabel", {}).get("value")

    return {
        "identifier": org_id,
        "description": fila.get("orgDescription", {}).get("value"),
        "country_name": country_name,
        "country_identifier": country_id
    }
