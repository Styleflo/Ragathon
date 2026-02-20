import requests
import time
from pathlib import Path

URL_CSV_311 = "https://donnees.montreal.ca/dataset/5866f832-676d-4b07-be6a-e99c21eb17e4/resource/2cfa0e06-9be4-49a6-b7f1-ee9f2363a872/download/requetes311.csv"

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


if __name__ == "__main__":
    csv311_reload()