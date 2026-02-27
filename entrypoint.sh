#!/bin/bash
set -e

#echo "--- Téléchargement des données 311 et Météo ---"
#python src/helper/csv_reloader.py
#
#echo "--- Téléchargement des données GTFS STM ---"
#python src/helper/download_gtfs_static_stm.py --skip-if-same

echo "--- Lancement de l'application Streamlit ---"
exec streamlit run src/frontend/Copilot.py --server.port=8080 --server.address=0.0.0.0