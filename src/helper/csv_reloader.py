from datetime import datetime
from pathlib import Path
from io import BytesIO
import pandas as pd
import requests
import time

URL_CSV_311 = "https://donnees.montreal.ca/dataset/5866f832-676d-4b07-be6a-e99c21eb17e4/resource/2cfa0e06-9be4-49a6-b7f1-ee9f2363a872/download/requetes311.csv"
URL_WEATHER = "https://climate.weather.gc.ca/climate_data/bulk_data_f.html"

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR.parent

DATA_DIR = SRC_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

csv_path = DATA_DIR / "requetes311.csv"


def csv311_reload():
    start = time.time()
    response = requests.get(URL_CSV_311)
    end = time.time()

    print(f"réponse complète en : {end - start:.2f} secondes")

    if response.status_code == 200:
        csv_path.write_bytes(response.content)
        print(f"✅ Fichier téléchargé avec succès → {csv_path}")
    else:
        print("❌ Erreur :", response.status_code)


def download_weather_csv(station_id, start_year=2022):
    all_data = []

    current_year = datetime.now().year
    nb = current_year - (start_year - 1)

    for i in range(0, nb):

        params = {
            "format": "csv",  # On veut du CSV
            "stationID": station_id,  # 51157 pour Montréal
            "Year": f"{start_year + i}",
            "Month": "1",
            "Day": "1",
            "timeframe": "2",  # 2 correspond aux données quotidiennes
            "submit": "Download Data"
        }

        print(f"Téléchargement des données pour la station {station_id} ({start_year + i})...")

        response = requests.get(URL_WEATHER, params=params)
        if response.status_code == 200:
            data = pd.read_csv(BytesIO(response.content))
            all_data.append(data)
        else:
            print(f"Erreur lors du téléchargement : {response.status_code}")

    if all_data:

        final_df = pd.concat(all_data, ignore_index=True)

        # Sauvegarde unique
        output_file = DATA_DIR / f"meteo_montreal.csv"
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\nEnregistrement terminé ! {len(final_df)} jours enregistrés dans {output_file}")
    else:
        print("Aucune donnée n'a pu être récupérée.")

if __name__ == "__main__":
    # Exemple d'utilisation pour Montréal, Février 2026
    download_weather_csv("51157", 2023)