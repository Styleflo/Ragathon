import chromadb
import pandas as pd
from pathlib import Path

# Get the directory where this script is located (src/services/)
# Then go up one level to get src/
BASE_DIR = Path(__file__).resolve().parent.parent

datasets = {
    "requetes311": {
        "df": pd.read_csv(BASE_DIR / "data/requetes311.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path=str(BASE_DIR / "db_requetes311")).get_or_create_collection("requetes311_rag"),
        "description_file": str(BASE_DIR / "desc/requetes311.md")
    },
    "collisions_routieres": {
        "df": pd.read_csv(BASE_DIR / "data/collisions_routieres.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path=str(BASE_DIR / "db_collisions_routieres")).get_or_create_collection("collisions_routieres_rag"),
        "description_file": str(BASE_DIR / "desc/collisions_routieres.md")
    },
    "gtfs_stm": {
        "df": pd.read_csv(BASE_DIR / "data/gtfs_stm.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path=str(BASE_DIR / "db_gtfs_stm")).get_or_create_collection("gtfs_stm_rag"),
        "description_file": str(BASE_DIR / "desc/gtfs_columns.md")
    },
    "meteo_montreal": {
        "df": pd.read_csv(BASE_DIR / "data/meteo_montreal.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path=str(BASE_DIR / "db_meteo_montreal")).get_or_create_collection("meteo_montreal_rag"),
        "description_file": str(BASE_DIR / "desc/contexte_metier_meteo.md")
    }
}

requetes311 = datasets["requetes311"]["df"]
collisions_routieres = datasets["collisions_routieres"]["df"]
gtfs_stm = datasets["gtfs_stm"]["df"]
meteo_montreal = datasets["meteo_montreal"]["df"]