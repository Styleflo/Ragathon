from services.datasets_info import requetes311, collisions_routieres
from folium.plugins import FastMarkerCluster
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import pandas as pd
import folium


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


def nuage_point_311(date_debut='2020-01-01', date_fin='2020-03-31'):
    data311 = requetes311.copy()

    data_sample = data311.dropna(subset=['LOC_LAT', 'LOC_LONG', 'ACTI_NOM'])
    data_sample = data_sample[
        (data_sample["DDS_DATE_CREATION"] >= date_debut) &
        (data_sample["DDS_DATE_CREATION"] <= date_fin)]

    if not data_sample.empty:
        data_sample = data_sample.sample(n=30000)

    data_list = data_sample[['LOC_LAT', 'LOC_LONG', 'ACTI_NOM']].values.tolist()

    m_nuage = folium.Map(location=[45.5017, -73.5673], zoom_start=11)

    callback = """
        function (row) {
            var circle = L.circleMarker([row[0], row[1]], {
                radius: 3,
                color: 'blue',
                fillColor: 'blue',
                fillOpacity: 0.6
            });
            circle.bindPopup("<b>Motif :</b> " + row[2]); 
            return circle;
        }
    """

    FastMarkerCluster(
        data=data_list,
        callback=callback
    ).add_to(m_nuage)

    return m_nuage._repr_html_()

def correlation_meteo_incident(date_debut = '2020-01-01', date_fin = '2021-03-31'):

    etat_meteo_map = {'11': 'Clair', '13': 'Brouillard', '14': 'Pluie', '17': 'Neige', '18': 'Poudrerie', '19': 'Verglas'}

    data_plot = collisions_routieres.copy()
    data_plot = data_plot.dropna(subset=["CD_COND_METEO", "GRAVITE"])

    data_plot = data_plot[(data_plot['DT_ACCDN'] >= date_debut) & (data_plot['DT_ACCDN'] <= date_fin)]
    if data_plot.empty:
        return "None"

    data_plot["CD_COND_METEO"] = data_plot["CD_COND_METEO"].astype(float).astype(int).astype(str)
    data_plot['Etat_meteo_Label'] = data_plot['CD_COND_METEO'].map(etat_meteo_map)

    data_plot = data_plot.dropna(subset=["Etat_meteo_Label"])


    ct = pd.crosstab(data_plot['Etat_meteo_Label'], data_plot['GRAVITE'], normalize='index') * 100
    ordre_meteo = ['Clair', 'Brouillard', 'Pluie', 'Neige', 'Poudrerie', 'Verglas']
    ct = ct.reindex(ordre_meteo)

    fig, ax = plt.subplots(figsize=(12, 7))

    # On passe l'objet 'ax' au plot de pandas
    ct.plot(kind='bar', stacked=True, colormap='magma', width=0.8, ax=ax)

    ax.set_title('Répartition (%) de la Gravité selon la Météo', fontsize=15, pad=20)
    ax.set_xlabel('Condition météo', fontsize=12)
    ax.set_ylabel("Pourcentage d'accidents (%)", fontsize=12)
    ax.set_ylim(0, 110)
    plt.xticks(rotation=0)  # Fonctionne toujours ou utiliser ax.set_xticklabels

    ax.legend(title='Gravité', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Annotation (inchangé mais utilise ax.patches)
    for p in ax.patches:
        height = p.get_height()
        if height > 5:
            x, y = p.get_xy()
            ax.annotate(f'{height:.1f}%', (x + p.get_width() / 2, y + height / 2),
                        ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    fig.tight_layout()

    return fig
