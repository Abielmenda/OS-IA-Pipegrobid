import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent

ONLINE_ENRICHMENT_SCRIPT = ROOT_DIR / "online_enrichment" / "scripts" / "enrich_online.py"
LOCAL_KG_SCRIPT = ROOT_DIR / "gen_local_kg" / "scripts" / "local_kg.py"


def run_script(script_path: Path):
    """
    Ejecuta un script de Python usando el mismo intérprete con el que se lanza este main.
    """

    if not script_path.exists():
        raise FileNotFoundError(f"No se encontró el script: {script_path}")

    print(f"\nEjecutando: {script_path.name}")
    print(f"Ruta: {script_path}")

    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=script_path.parent,
        check=True
    )


def main():
    print("========================================")
    print("STEP 4 - Enriquecimiento + KG local")
    print("========================================")

    # 1. Primero enriquecemos los JSONs online
    run_script(ONLINE_ENRICHMENT_SCRIPT)

    # 2. Después generamos el KG local con los JSONs ya enriquecidos
    run_script(LOCAL_KG_SCRIPT)

    print("\n========================================")
    print("Proceso completo finalizado correctamente")
    print("========================================")


if __name__ == "__main__":
    main()