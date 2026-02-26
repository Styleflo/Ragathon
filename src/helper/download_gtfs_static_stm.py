#!/usr/bin/env python3
"""
download_gtfs_static_stm.py

- Télécharge le zip GTFS static STM
- Dézippe dans un dossier temporaire
- Remplace les fichiers *.txt dans un dossier cible (ex: src/data)
- Vérifie si les fichiers existent déjà (et peut skip si identiques)
- Écriture atomique (évite les fichiers corrompus si quelqu’un lit en même temps)
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable, Optional

import requests


DEFAULT_URL = "https://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip"

# Chemin absolu vers src/ (parent de helper/)
SRC_DIR = Path(__file__).resolve().parent.parent
DEFAULT_OUT_DIR = SRC_DIR / "data"
DEFAULT_CACHE_ZIP = SRC_DIR / "data" / "_cache" / "gtfs_stm.zip"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_file(url: str, dest: Path, timeout: int = 60) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Stream download -> écrit d'abord en .tmp puis rename atomique
    tmp = dest.with_suffix(dest.suffix + ".tmp")

    with requests.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        with tmp.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)
            f.flush()
            os.fsync(f.fileno())

    tmp.replace(dest)  # atomic rename (Linux/WSL)


def safe_replace_file(src: Path, dst: Path) -> None:
    """
    Remplace dst par src de manière atomique.
    Copie src -> dst.tmp puis replace.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(dst.suffix + ".tmp")
    shutil.copy2(src, tmp)
    # flush/sync best effort
    with tmp.open("rb") as f:
        os.fsync(f.fileno())
    tmp.replace(dst)


def iter_txt_files(folder: Path) -> Iterable[Path]:
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() == ".txt":
            yield p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default=DEFAULT_URL, help="URL du zip GTFS")
    ap.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Dossier cible où copier les .txt (créé si absent)",
    )
    ap.add_argument(
        "--cache-zip",
        default=str(DEFAULT_CACHE_ZIP),
        help="Chemin local pour stocker le zip téléchargé",
    )
    ap.add_argument(
        "--skip-if-same",
        action="store_true",
        help="Si activé, ne remplace un fichier .txt que si son hash diffère",
    )
    ap.add_argument(
        "--backup",
        action="store_true",
        help="Si activé, sauvegarde l'ancien fichier en .bak avant remplacement",
    )
    args = ap.parse_args()

    url = args.url
    out_dir = Path(args.out_dir)
    zip_path = Path(args.cache_zip)

    print(f"→ Download: {url}")
    download_file(url, zip_path)
    print(f"✓ ZIP saved: {zip_path} ({zip_path.stat().st_size} bytes)")

    with tempfile.TemporaryDirectory(prefix="gtfs_stm_") as td:
        extract_dir = Path(td) / "unzipped"
        extract_dir.mkdir(parents=True, exist_ok=True)

        print(f"→ Unzip to: {extract_dir}")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)

        txt_files = list(iter_txt_files(extract_dir))
        if not txt_files:
            print("✗ Aucun fichier .txt trouvé dans le zip. (Zip inattendu ?)")
            return 2

        out_dir.mkdir(parents=True, exist_ok=True)

        replaced = 0
        skipped = 0

        for src in txt_files:
            # Dans le zip STM, les fichiers sont souvent au root. On garde le nom de fichier.
            dst = out_dir / src.name

            if dst.exists() and args.skip_if_same:
                try:
                    if sha256_file(src) == sha256_file(dst):
                        skipped += 1
                        continue
                except Exception:
                    # si hash fail, on remplace quand même
                    pass

            if dst.exists() and args.backup:
                bak = dst.with_suffix(dst.suffix + ".bak")
                shutil.copy2(dst, bak)

            safe_replace_file(src, dst)
            replaced += 1

        print(f"✓ Done. Replaced: {replaced} | Skipped: {skipped}")
        print(f"→ Output folder: {out_dir.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())