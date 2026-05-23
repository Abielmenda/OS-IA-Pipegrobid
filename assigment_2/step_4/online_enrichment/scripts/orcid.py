import requests

# ORCID necesita Accept: application/json o devuelve XML en vez de JSON
HEADERS = {
    "Accept": "application/json"
}

def enrich_person(nombre_completo):
    # Solo podemos buscar personas con nombre completo.
    # Las iniciales como "S.G." o "CJP" no se pueden buscar en ORCID.
    partes = nombre_completo.strip().split()
    if len(partes) < 2:
        return None

    nombre = partes[0]
    apellido = partes[-1]

    # Paso 1: buscamos el ORCID ID por nombre y apellido
    url_busqueda = f"https://pub.orcid.org/v3.0/search?q=family-name:{apellido}+AND+given-names:{nombre}"
    respuesta = requests.get(url_busqueda, headers=HEADERS)
    datos = respuesta.json()

    if datos.get("num-found", 0) == 0:
        return None

    orcid_id = datos["result"][0]["orcid-identifier"]["path"]

    # Paso 2: con el ORCID ID obtenemos el perfil completo para sacar la afiliación.
    # Necesitamos una segunda llamada porque la búsqueda solo devuelve el ID.
    url_perfil = f"https://pub.orcid.org/v3.0/{orcid_id}/record"
    respuesta2 = requests.get(url_perfil, headers=HEADERS)
    datos2 = respuesta2.json()

    # La afiliación está en el primer empleo registrado en ORCID.
    # Si la persona no tiene empleos registrados la afiliación queda como None.
    afiliacion = None
    empleos = datos2.get("activities-summary", {}).get("employments", {}).get("affiliation-group", [])
    if empleos:
        empleo = empleos[0].get("summaries", [{}])[0].get("employment-summary", {})
        org = empleo.get("organization", {})
        afiliacion = org.get("name")

    return {
        "identifier": orcid_id,
        "affiliation": afiliacion
    }
