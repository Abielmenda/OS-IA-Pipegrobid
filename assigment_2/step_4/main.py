import shutil
import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent

ONLINE_ENRICHMENT_DIR = ROOT_DIR / "online_enrichment"
LOCAL_KG_DIR = ROOT_DIR / "gen_local_kg"

PIPELINE = [
    (ONLINE_ENRICHMENT_DIR, Path("scripts") / "enrich_online.py"),
    (LOCAL_KG_DIR, Path("scripts") / "local_kg.py"),
]


def build_python_command(project_dir: Path, script: Path) -> list[str]:
    poetry = shutil.which("poetry")

    if poetry and (project_dir / "pyproject.toml").exists():
        return [poetry, "run", "python", str(script)]

    return [sys.executable, str(project_dir / script)]


def ensure_dependencies(project_dir: Path):
    poetry = shutil.which("poetry")

    if not poetry or not (project_dir / "pyproject.toml").exists():
        return

    subprocess.run([poetry, "install", "--no-root"], cwd=project_dir, check=True)


def run_script(project_dir: Path, script: Path):
    script_path = project_dir / script

    if not script_path.exists():
        raise FileNotFoundError(f"No se encontro el script: {script_path}")

    ensure_dependencies(project_dir)
    command = build_python_command(project_dir, script)

    print(f"\nEjecutando: {script_path.name}")
    print(f"Ruta: {script_path}")
    print(f"Comando: {subprocess.list2cmdline(command)}")

    subprocess.run(command, cwd=project_dir, check=True)


def main():
    print("========================================")
    print("STEP 4 - Enriquecimiento + KG local")
    print("========================================")

    for project_dir, script in PIPELINE:
        run_script(project_dir, script)

    print("\n========================================")
    print("Proceso completo finalizado correctamente")
    print("========================================")


if __name__ == "__main__":
    main()
