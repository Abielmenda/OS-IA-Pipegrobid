import json
import re
import shutil
from pathlib import Path
from openaire import enrich_project
from wikidata import enrich_organization
from orcid import enrich_person

# Leemos los JSONs generados por enrich_jsons.py del topic_modeling
# y guardamos los JSONs enriquecidos en una carpeta nueva kg_enriched
ROOT = Path(__file__).resolve().parents[4]
INPUT_DIR = ROOT / "assigment_2" / "step_3" / "outputs" / "topics" / "enriched_jsons"
OUTPUT_DIR = ROOT / "assigment_2" / "step_3" / "outputs" / "topics" / "kg_enriched"

def limpiar_grant_id(texto):
    # Extraemos el código real del identificador del proyecto.
    # El LLM a veces devuelve cosas como "grant agreement No. 851173"
    # y necesitamos quedarnos solo con "851173".
    patrones = [
        r'\b[A-Z]{2,}[\/\-][A-Z0-9][A-Z0-9\/\-]+\b',  # EP/S023356/1, IIS-2229876
        r'\b\d{2,}-\d+[A-Z]?\b',                        # 26-23955S
        r'\b\d{5,}\b',                                   # 851173
    ]
    for patron in patrones:
        resultado = re.search(patron, texto.upper())
        if resultado:
            return resultado.group()
    return None

def enrich_json(data):

    # --- Proyectos con OpenAIRE ---
    # Limpiamos el identificador y consultamos OpenAIRE.
    # Los identificadores que no son códigos reales (ej: "Horizon 2020") se descartan.
    proyectos_validos = []
    for proyecto in data.get("projects", []):
        grant_id = limpiar_grant_id(proyecto.get("identifier", ""))
        if not grant_id:
            continue
        print(f"  OpenAIRE: {grant_id}")
        resultado = enrich_project(grant_id)
        if resultado:
            proyecto.update(resultado)
        proyectos_validos.append(proyecto)
    data["projects"] = proyectos_validos

    # --- Organizaciones con Wikidata ---
    # Quitamos el acrónimo entre paréntesis antes de buscar.
    # Ej: "European Research Council (ERC)" -> "European Research Council"
    # Guardamos los países encontrados para crear los nodos Country.
    paises = {}
    for org in data.get("organizations", []):
        nombre = re.sub(r'\s*\(.*?\)', '', org.get("name", "")).strip()
        print(f"  Wikidata: {nombre}")
        resultado = enrich_organization(nombre)
        if resultado:
            org["identifier"] = resultado["identifier"]
            org["description"] = resultado["description"]
            if resultado.get("country_name") and resultado.get("country_identifier"):
                paises[resultado["country_name"]] = resultado["country_identifier"]
                org["country"] = resultado["country_name"]

    # --- Nodos Country ---
    # Creamos un nodo Country por cada país encontrado.
    # Descartamos "Internationality" porque no es un país real
    # (Wikidata lo devuelve para organizaciones supranacionales como la UE).
    data["countries"] = [
        {"name": nombre, "identifier": identifier}
        for nombre, identifier in paises.items()
        if nombre and nombre != "Internationality"
    ]

    # --- Personas con ORCID ---
    # Quitamos el campo orcid antiguo que venía vacío del pipeline anterior.
    # Solo buscamos personas con nombre completo (mínimo nombre y apellido).
    for persona in data.get("people", []):
        persona.pop("orcid", None)
        nombre = persona.get("name", "")
        if len(nombre.split()) >= 2:
            print(f"  ORCID: {nombre}")
            resultado = enrich_person(nombre)
            if resultado:
                persona["identifier"] = resultado["identifier"]
                persona["affiliation"] = resultado["affiliation"]

    return data

def main():
    if not INPUT_DIR.exists():
        print(f"ERROR: No existe la carpeta: {INPUT_DIR}")
        print("Debes ejecutar primero enrich_jsons.py del topic_modeling")
        return

    # Creamos la carpeta de salida desde cero
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    json_files = sorted(INPUT_DIR.glob("*.json"))
    print(f"JSONs encontrados: {len(json_files)}")

    for json_file in json_files:
        print(f"\nProcesando: {json_file.name}")
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        data_enriquecida = enrich_json(data)

        output_file = OUTPUT_DIR / json_file.name
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data_enriquecida, f, ensure_ascii=False, indent=2)

        print(f"  Guardado en: {output_file}")

if __name__ == "__main__":
    main()
