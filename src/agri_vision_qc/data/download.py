"""Descarga y verificación del Lemons quality control dataset (SoftwareMill).

Ejecutar desde la carpeta raíz del proyecto:

    uv run python -m agri_vision_qc.data.download

Pasos: descarga el ZIP (si no está ya), comprueba su huella SHA-256,
lo descomprime y verifica que las anotaciones COCO y las imágenes cuadran.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path

import requests
from tqdm import tqdm

URL = "https://github.com/softwaremill/lemon-dataset/raw/master/data/lemon-dataset.zip"

# Huella SHA-256 del ZIP. 
# Se ha dejado vacía hasta la primera descarga: el script la calcula y la muestra, 
# y después se copia aquí para "fijar" el dataset.
# EXPECTED_SHA256 = ""
EXPECTED_SHA256 = "b208bb2c68b89bc4e23fc7a7e009bac0f6dc3529351346582548d48eacd502f7"

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}


def sha256_of(path: Path) -> str:
    """Calcula la huella SHA-256 de un archivo leyéndolo por bloques."""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, dest: Path) -> None:
    """Descarga a un archivo .part y solo lo renombra cuando ha terminado bien."""
    part = dest.with_name(dest.name + ".part")
    with requests.get(url, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("Content-Length", 0)) or None
        with part.open("wb") as f, tqdm(
            total=total, unit="B", unit_scale=True, desc="Descargando"
        ) as bar:
            for chunk in resp.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
                bar.update(len(chunk))
    part.replace(dest)


def is_junk(path: Path) -> bool:
    """Archivos que añade macOS al comprimir y que no son datos."""
    return "__MACOSX" in path.parts or path.name.startswith("._")


def verify(extract_dir: Path) -> None:
    """Comprueba que cada imagen de las anotaciones existe en disco y resume el contenido."""
    ann_files = [p for p in extract_dir.rglob("instances_default.json") if not is_junk(p)]
    if not ann_files:
        sys.exit(f"ERROR: no encuentro 'instances_default.json' dentro de {extract_dir}")
    ann_path = ann_files[0]
    coco = json.loads(ann_path.read_text(encoding="utf-8"))

    images = coco["images"]
    annotations = coco["annotations"]
    categories = {c["id"]: c["name"] for c in coco["categories"]}

    on_disk = {
        p.name: p
        for p in extract_dir.rglob("*")
        if p.suffix.lower() in IMAGE_SUFFIXES and not is_junk(p)
    }
    missing = [img["file_name"] for img in images if Path(img["file_name"]).name not in on_disk]

    per_category = Counter(categories[a["category_id"]] for a in annotations)
    #lemons = Counter(Path(img["file_name"]).name.split("_")[0] for img in images)
    image_dirs = sorted({str(p.parent.relative_to(extract_dir)) for p in on_disk.values()})

    print("\n=== Verificación del dataset ===")
    print(f"Anotaciones COCO:        {ann_path.relative_to(extract_dir)}")
    print(f"Carpeta(s) de imágenes:  {', '.join(image_dirs)}")
    print(f"Imágenes en el JSON:     {len(images)}")
    print(f"Imágenes en disco:       {len(on_disk)}")
    print(f"Imágenes que faltan:     {len(missing)}")
    print(f"Regiones anotadas:       {len(annotations)}")
    #print(f"Limones distintos:       {len(lemons)} "
    #      f"(fotos por limón: mín {min(lemons.values())}, máx {max(lemons.values())})")
    print("Regiones por categoría:")
    for name, count in per_category.most_common():
        print(f"  {name:<22}{count:>6}")
    print(f"Ejemplo de nombre:       {Path(images[0]['file_name']).name}")

    if missing:
        print("\nPrimeras imágenes que faltan:", *missing[:5], sep="\n  ")
        sys.exit("ERROR: faltan imágenes; borra la carpeta descomprimida y vuelve a ejecutar.")
    print("\nOK: todas las imágenes de las anotaciones están en disco.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dest", type=Path, default=Path("data/raw"),
                        help="carpeta de destino (por defecto: data/raw)")
    parser.add_argument("--url", default=URL, help=argparse.SUPPRESS)
    args = parser.parse_args()

    raw_dir = args.dest.resolve()
    raw_dir.mkdir(parents=True, exist_ok=True)
    zip_path = raw_dir / "lemon-dataset.zip"
    extract_dir = raw_dir / "lemon-dataset"
    print(f"Destino: {raw_dir}")

    # 1. Descarga (solo si no está ya)
    if zip_path.exists():
        print("El ZIP ya está descargado; no se vuelve a descargar.")
    else:
        download(args.url, zip_path)

    # 2. Integridad: la huella debe coincidir con la fijada
    digest = sha256_of(zip_path)
    print(f"SHA-256: {digest}")
    if not EXPECTED_SHA256:
        print("AVISO: aún no hay huella fijada. Copia la línea SHA-256 de arriba en "
              "EXPECTED_SHA256 (download.py) para fijar esta versión del dataset.")
    elif digest != EXPECTED_SHA256:
        sys.exit("ERROR: la huella no coincide. Borra el ZIP y vuelve a ejecutar el script.")
    else:
        print("OK: la huella coincide con la fijada.")

    # 3. Descompresión (solo si no está ya), en una carpeta temporal que se
    #    renombra al final: si se interrumpe, la próxima vez se repite entera.
    if extract_dir.exists():
        print("El dataset ya está descomprimido.")
    else:
        print("Descomprimiendo...")
        tmp_dir = raw_dir / "lemon-dataset.tmp"
        shutil.rmtree(tmp_dir, ignore_errors=True)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp_dir)
        # Si el ZIP trae una única carpeta raíz, esa es el dataset (evita lemon-dataset/lemon-dataset)
        entries = [p for p in tmp_dir.iterdir() if not is_junk(p)]
        root = entries[0] if len(entries) == 1 and entries[0].is_dir() else tmp_dir
        root.rename(extract_dir)
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # 4. Verificación del contenido
    verify(extract_dir)


if __name__ == "__main__":
    main()