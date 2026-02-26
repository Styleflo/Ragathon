"""
Génère la synthèse top 5 et la sauvegarde dans un fichier.
Lancer ce script quand vous voulez mettre à jour la synthèse.

Usage: python generate_synthesis.py
"""

from pathlib import Path
from datetime import datetime
import sys
import time
from services.models import LANGUAGE_MODEL

# Add src to path
SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from answer import get_top5

SYNTHESIS_FILE = SRC_DIR / "frontend" / "synthesis_cache_grand_public.md"
SYNTHESIS_FILE_MUNICIPALITE = SRC_DIR / "frontend" / "synthesis_cache_municipalite.md"


def backup_if_exists(filepath: Path):
    """Backup existing file to .bak if it exists."""
    if filepath.exists():
        backup_path = filepath.with_suffix(".md.bak")
        filepath.rename(backup_path)
        print(f"  → Backup créé: {backup_path.name}")


def save_with_date(filepath: Path, content: str):
    """Save content with generation date header."""
    date_header = f"<!-- Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n"
    filepath.write_text(date_header + content, encoding="utf-8")


def generate_and_save():
    print("Génération de la synthèse en cours...")
    
    # Grand public
    print("\n[Grand public]")
    backup_if_exists(SYNTHESIS_FILE)
    synthesis_grand_public = get_top5(tone="grand public")
    save_with_date(SYNTHESIS_FILE, synthesis_grand_public)
    print(f"✓ Synthèse sauvegardée dans: {SYNTHESIS_FILE}")
    print(f"  Taille: {len(synthesis_grand_public)} caractères")

    # Municipalité
    print("\n[Municipalité]")
    backup_if_exists(SYNTHESIS_FILE_MUNICIPALITE)
    synthesis_municipalité = get_top5(tone="municipalité")
    save_with_date(SYNTHESIS_FILE_MUNICIPALITE, synthesis_municipalité)
    print(f"✓ Synthèse municipale sauvegardée dans: {SYNTHESIS_FILE_MUNICIPALITE}")
    print(f"  Taille: {len(synthesis_municipalité)} caractères")


if __name__ == "__main__":
    start_time = time.time()
    generate_and_save()
    end_time = time.time()
    print(f"\nTemps total de génération: {end_time - start_time:.2f} secondes with {LANGUAGE_MODEL}")
