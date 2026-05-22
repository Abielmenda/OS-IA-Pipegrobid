from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


STEP_DIR = Path(__file__).resolve().parent
XMLS_PARSE_DIR = STEP_DIR / "xmls_parse"
NER_EXTRACTION_DIR = STEP_DIR / "ner_extraction"
PARSED_JSONS_DIR = STEP_DIR / "outputs" / "parsed_xmls"

PIPELINE = [
    (XMLS_PARSE_DIR, Path("parse_grobid_xml.py")),
    (NER_EXTRACTION_DIR, Path("scripts") / "llama_extraction.py"),
]


def _build_python_command(project_dir: Path, script: Path) -> list[str]:
    poetry = shutil.which("poetry")

    if poetry and (project_dir / "pyproject.toml").exists():
        return [poetry, "run", "python", str(script)]

    return [sys.executable, str(project_dir / script)]


def _run_script(project_dir: Path, script: Path) -> None:
    script_path = project_dir / script

    if not script_path.exists():
        raise FileNotFoundError(f"No existe el script: {script_path}")

    command = _build_python_command(project_dir, script)
    print(f"\n==> Ejecutando: {subprocess.list2cmdline(command)}")
    subprocess.run(command, cwd=project_dir, check=True)


def _ensure_inputs() -> None:
    if not PARSED_JSONS_DIR.exists() or not any(PARSED_JSONS_DIR.glob("*.json")):
        raise FileNotFoundError(
            "No hay JSONs parseados en "
            f"{PARSED_JSONS_DIR}. Ejecuta primero el parseo de XMLs."
        )


def main() -> None:
    print("Step 2 - parseo XML y extraccion NER de acknowledgements")

    xmls_parse_step, ner_extraction_step = PIPELINE

    _run_script(*xmls_parse_step)
    _ensure_inputs()
    _run_script(*ner_extraction_step)

    print("\nStep 2 completado.")


if __name__ == "__main__":
    main()
