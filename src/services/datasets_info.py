import chromadb
import pandas as pd

datasets = {
    "requetes311": {
        "df": pd.read_csv("data/requetes311.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_requetes311").get_or_create_collection("requetes311_rag"),
        "description_file": "desc/requetes311.md"
    },
    "collisions_routieres": {
        "df": pd.read_csv("data/collisions_routieres.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_collisions_routieres").get_or_create_collection("collisions_routieres_rag"),
        "description_file": "desc/collisions_routieres.md"
    },
    "gtfs_stm": {
        "df": pd.read_csv("data/gtfs_stm.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_gtfs_stm").get_or_create_collection("gtfs_stm_rag"),
        "description_file": "desc/gtfs_columns.md"
    },
    "meteo_montreal": {
        "df": pd.read_csv("data/meteo_montreal.csv", low_memory=False),
        "collection": chromadb.PersistentClient(path="db_meteo_montreal").get_or_create_collection("meteo_montreal_rag"),
        "description_file": "desc/contexte_metier_meteo.md"
    }
}

requetes311 = datasets["requetes311"]["df"]
collisions_routieres = datasets["collisions_routieres"]["df"]
gtfs_stm = datasets["gtfs_stm"]["df"]
meteo_montreal = datasets["meteo_montreal"]["df"]