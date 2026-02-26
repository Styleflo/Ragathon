import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
from services.datasets_info import requetes311, collisions_routieres

def heatmap_collisions_filtree(date_debut='2020-01-01', date_fin='2020-03-31'):
    data_collision = collisions_routieres.copy()
    data_collision['DT_ACCDN'] = pd.to_datetime(data_collision['DT_ACCDN'])

    data_filtered = data_collision[(data_collision['DT_ACCDN'] >= date_debut) &
                                   (data_collision['DT_ACCDN'] <= date_fin)]

    # 3. Nettoyage des données filtrées
    # On retire les lignes où les coordonnées sont manquantes
    data_clean2 = data_filtered.dropna(subset=['LOC_LAT', 'LOC_LONG'])

    # 4. Initialisation de la carte centrée sur Montréal
    montreal_coords = [45.5017, -73.5673]
    m2 = folium.Map(location=montreal_coords, zoom_start=11)

    # 5. Préparation et ajout de la Heatmap
    heat_data2 = data_clean2[['LOC_LAT', 'LOC_LONG']].values.tolist()
    HeatMap(heat_data2, radius=10, blur=15, min_opacity=0.5).add_to(m2)

    return m2._repr_html_()
