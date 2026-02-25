import chromadb
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "sqlite_db" / "mobility.db"

TABLES = ["requetes311", "collisions_routieres", "gtfs_stm", "meteo_montreal"]

def get_db_connection():
    """Get a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

datasets = {
    "requetes311": {
        "table": "requetes311",
        "collection": chromadb.PersistentClient(path=str(BASE_DIR / "db_requetes311")).get_or_create_collection("requetes311_rag"),
        "description_file": str(BASE_DIR / "desc/requetes311.md")
    },
    "collisions_routieres": {
        "table": "collisions_routieres",
        "collection": chromadb.PersistentClient(path=str(BASE_DIR / "db_collisions_routieres")).get_or_create_collection("collisions_routieres_rag"),
        "description_file": str(BASE_DIR / "desc/collisions_routieres.md")
    },
    "gtfs_stm": {
        "table": "gtfs_stm",
        "collection": chromadb.PersistentClient(path=str(BASE_DIR / "db_gtfs_stm")).get_or_create_collection("gtfs_stm_rag"),
        "description_file": str(BASE_DIR / "desc/gtfs_columns.md")
    },
    "meteo_montreal": {
        "table": "meteo_montreal",
        "collection": chromadb.PersistentClient(path=str(BASE_DIR / "db_meteo_montreal")).get_or_create_collection("meteo_montreal_rag"),
        "description_file": str(BASE_DIR / "desc/contexte_metier_meteo.md")
    }
}