import streamlit as st
from datetime import date
import streamlit.components.v1 as components
from services.graph import heatmap_collisions_filtree, correlation_meteo_incident, nuage_point_311, accidents_histogramme

st.set_page_config(page_title=" Dashboard - Montréal", page_icon="🗺️", layout="wide")
st.title("🗺️ Dashboard - Montréal")

with st.sidebar:
    st.header("Période")

    date_debut_object = st.date_input("Date de début", value=date(2015, 1, 1), min_value=date(2000, 1, 1), max_value=date.today())
    date_fin_object = st.date_input("Date de fin", value=date.today(), min_value=date(2000, 1, 1), max_value=date.today())
    date_debut = str(date_debut_object)
    date_fin = str(date_fin_object)

    # Remplacer par les fonctions qui génèrent les graphiques en fonction des dates sélectionnées
    if "html_code_1" not in st.session_state:
        st.session_state.html_code_1 = heatmap_collisions_filtree(date_debut, date_fin)
        st.session_state.html_code_2 = nuage_point_311(date_debut, date_fin)
        st.session_state.fig_3 = correlation_meteo_incident(date_debut, date_fin)
        st.session_state.fig_4 = accidents_histogramme(date_debut, date_fin)

    is_valid_date = date_debut > date_fin
    if is_valid_date:
        st.error("La date de début doit être antérieure à la date de fin.")

    if st.button("Afficher les données", disabled=is_valid_date, width="stretch"):
        st.session_state.date_debut = date_debut
        st.session_state.date_fin = date_fin

        # Remplacer par les fonctions qui génèrent les graphiques en fonction des dates sélectionnées
        st.session_state.html_code_1 = heatmap_collisions_filtree(date_debut, date_fin)
        st.session_state.html_code_2 = nuage_point_311(date_debut, date_fin)
        st.session_state.fig_3 = correlation_meteo_incident(date_debut, date_fin)
        st.session_state.fig_4 = accidents_histogramme(date_debut, date_fin)

        st.rerun()

with st.container():
    st.subheader("Heatmap des collisions")
    st.caption("Répartition des collisions à Montréal en fonction de la période sélectionnée.")
    if st.session_state.html_code_1 == "None":
        st.warning("Aucune donnée disponible pour la période sélectionnée.")
    else:
        components.html(st.session_state.html_code_1, height=500)

st.divider() 

with st.container():
    st.subheader("Graphique 2") #Titre a modifier
    st.caption("Description du graphique 2.") # Description a modifier
    if st.session_state.html_code_2 == "None":
        st.warning("Aucune donnée disponible pour la période sélectionnée.")
    else:
        components.html(st.session_state.html_code_2, height=500)

st.divider()

with st.container():
    st.subheader("Répartition (%) de la Gravité selon la Météo")
    st.caption("Description du graphique 3.") # Description a modifier
    if st.session_state.fig_3 == "None":
        st.warning("Aucune donnée disponible pour la période sélectionnée.")
    else:
        st.pyplot(st.session_state.fig_3)

st.divider()

with st.container():
    if (date_fin_object - date_debut_object).days > 365:
        st.subheader("Nombre d'accidents par mois")
    else:
        st.subheader("Nombre d'accidents par jours")
    st.caption("Description du graphique 4.") # Description a modifier
    if st.session_state.fig_4 == "None":
        st.warning("Aucune donnée disponible pour la période sélectionnée.")
    else:
        st.plotly_chart(st.session_state.fig_4)

st.divider()
