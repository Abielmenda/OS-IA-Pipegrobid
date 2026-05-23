import requests

def enrich_project(grant_id):
    # Consultamos la API de OpenAIRE con el código del proyecto.
    # Solo encuentra proyectos europeos principalmente.
    # Si no encuentra el proyecto devuelve None.
    url = f"https://api.openaire.eu/search/projects?grantID={grant_id}&format=json"
    respuesta = requests.get(url)
    datos = respuesta.json()

    total = datos["response"]["header"]["total"]["$"]
    if total == "0" or total == 0:
        return None

    proyecto = datos["response"]["results"]["result"][0]["metadata"]["oaf:entity"]["oaf:project"]

    return {
        "identifier": grant_id,
        "title": proyecto.get("title", {}).get("$"),
        "start_date": proyecto.get("startdate", {}).get("$"),
        "end_date": proyecto.get("enddate", {}).get("$"),
        "funding_amount": proyecto.get("fundedamount", {}).get("$"),
        "currency": proyecto.get("currency", {}).get("$"),
        "funder": proyecto.get("fundingtree", {}).get("funder", {}).get("name", {}).get("$")
    }
