import chromadb
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def _client(db_name: str):
    return chromadb.PersistentClient(path=str(BASE_DIR / db_name))

datasets = {
    "requetes311": {
        "df": pd.read_csv(BASE_DIR / "data/requetes311.csv", low_memory=False),
        "collection": _client("db_requetes311").get_or_create_collection("requetes311_rag"),
        "description_file": str(BASE_DIR / "desc/requetes311.md"),
    },
    "collisions_routieres": {
        "df": pd.read_csv(BASE_DIR / "data/collisions_routieres.csv", low_memory=False),
        "collection": _client("db_collisions_routieres").get_or_create_collection("collisions_routieres_rag"),
        "description_file": str(BASE_DIR / "desc/collisions_routieres.md"),
    },
    "meteo_montreal": {
        "df": pd.read_csv(BASE_DIR / "data/meteo_montreal.csv", low_memory=False),
        "collection": _client("db_meteo_montreal").get_or_create_collection("meteo_montreal_rag"),
        "description_file": str(BASE_DIR / "desc/contexte_metier_meteo.md"),
    },

    # -------- GTFS STATIC (1 table = 1 dataset) --------
    "agency": {
        "df": pd.read_csv(BASE_DIR / "data/agency.txt", low_memory=False),
        "collection": _client("db_agency").get_or_create_collection("agency_rag"),
        "description_file": str(BASE_DIR / "desc/agency.md"),
    },
    "calendar": {
        "df": pd.read_csv(BASE_DIR / "data/calendar.txt", low_memory=False),
        "collection": _client("db_calendar").get_or_create_collection("calendar_rag"),
        "description_file": str(BASE_DIR / "desc/calendar.md"),
    },
    "calendar_dates": {
        "df": pd.read_csv(BASE_DIR / "data/calendar_dates.txt", low_memory=False),
        "collection": _client("db_calendar_dates").get_or_create_collection("calendar_dates_rag"),
        "description_file": str(BASE_DIR / "desc/calendar_dates.md"),
    },
    "feed_info": {
        "df": pd.read_csv(BASE_DIR / "data/feed_info.txt", low_memory=False),
        "collection": _client("db_feed_info").get_or_create_collection("feed_info_rag"),
        "description_file": str(BASE_DIR / "desc/feed_info.md"),
    },
    "routes": {
        "df": pd.read_csv(BASE_DIR / "data/routes.txt", low_memory=False),
        "collection": _client("db_routes").get_or_create_collection("routes_rag"),
        "description_file": str(BASE_DIR / "desc/routes.md"),
    },
    "shapes": {
        "df": pd.read_csv(BASE_DIR / "data/shapes.txt", low_memory=False),
        "collection": _client("db_shapes").get_or_create_collection("shapes_rag"),
        "description_file": str(BASE_DIR / "desc/shapes.md"),
    },
    "stop_times": {
        "df": pd.read_csv(BASE_DIR / "data/stop_times.txt", low_memory=False),
        "collection": _client("db_stop_times").get_or_create_collection("stop_times_rag"),
        "description_file": str(BASE_DIR / "desc/stop_times.md"),
    },
    "stops": {
        "df": pd.read_csv(BASE_DIR / "data/stops.txt", low_memory=False),
        "collection": _client("db_stops").get_or_create_collection("stops_rag"),
        "description_file": str(BASE_DIR / "desc/stops.md"),
    },
    "trips": {
        "df": pd.read_csv(BASE_DIR / "data/trips.txt", low_memory=False),
        "collection": _client("db_trips").get_or_create_collection("trips_rag"),
        "description_file": str(BASE_DIR / "desc/trips.md"),
    },
    "translations": {
        "df": pd.read_csv(BASE_DIR / "data/translations.txt", low_memory=False),
        "collection": _client("db_translations").get_or_create_collection("translations_rag"),
        "description_file": str(BASE_DIR / "desc/translations.md"),
    },
}

requetes311 = datasets["requetes311"]["df"]
collisions_routieres = datasets["collisions_routieres"]["df"]
meteo_montreal = datasets["meteo_montreal"]["df"]

agency = datasets["agency"]["df"]
calendar = datasets["calendar"]["df"]
calendar_dates = datasets["calendar_dates"]["df"]
feed_info = datasets["feed_info"]["df"]
routes = datasets["routes"]["df"]
shapes = datasets["shapes"]["df"]
stop_times = datasets["stop_times"]["df"]
stops = datasets["stops"]["df"]
trips = datasets["trips"]["df"]
translations = datasets["translations"]["df"]

def get_datasets_metadata():
    result = {}
    for name, info in datasets.items():
        dataset = info["df"]
        cols = dataset.columns.tolist()
        result[name] = {"columns": cols}

    return result