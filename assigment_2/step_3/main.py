from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


STEP_DIR = Path(__file__).resolve().parent
TOPIC_MODELING_DIR = STEP_DIR / "topic_modeling"
INPUT_JSONS_DIR = (
    STEP_DIR.parent
    / "step_2"
    / "outputs"
    / "extrated_acknowledgements_parsed_xmls"
)

PIPELINE = [
    (TOPIC_MODELING_DIR, Path("scripts") / "topic_modeling.py"),
    (TOPIC_MODELING_DIR, Path("scripts") / "enrich_jsons.py"),
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
    if not INPUT_JSONS_DIR.exists() or not any(INPUT_JSONS_DIR.glob("*.json")):
        raise FileNotFoundError(
            "No hay JSONs enriquecidos del step 2 en "
            f"{INPUT_JSONS_DIR}. Ejecuta primero assigment_2/step_2/main.py."
        )


def main() -> None:
    print("Step 3 - topic modeling y enriquecimiento de JSONs")
    _ensure_inputs()

    for project_dir, script in PIPELINE:
        _run_script(project_dir, script)

    print("\nStep 3 completado.")


if __name__ == "__main__":
    main()
