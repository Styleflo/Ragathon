import streamlit as st
from datetime import date
import streamlit.components.v1 as components
from services.graph import heatmap_collisions_filtree, nuage_point_311, collisions_routieres

st.set_page_config(page_title=" Dashboard - Montréal", page_icon="🗺️", layout="wide")
st.title("🗺️ Dashboard - Montréal")

with st.sidebar:
    st.header("Période")

    date_debut = str(st.date_input("Date de début", value=date(2015, 1, 1)))
    date_fin = str(st.date_input("Date de fin", value=date.today()))


    # Remplacer par les fonctions qui génèrent les graphiques en fonction des dates sélectionnées
    if "html_code_1" not in st.session_state:
        st.session_state.html_code_1 = heatmap_collisions_filtree(date_debut, date_fin)
        st.session_state.html_code_2 = nuage_point_311(date_debut, date_fin)
        st.session_state.html_code_3 = heatmap_collisions_filtree(date_debut, date_fin)
        st.session_state.html_code_4 = heatmap_collisions_filtree(date_debut, date_fin)

    is_valid_date = date_debut > date_fin
    if is_valid_date:
        st.error("La date de début doit être antérieure à la date de fin.")

    if st.button("Afficher les données", disabled=is_valid_date, width="stretch"):
        st.session_state.date_debut = date_debut
        st.session_state.date_fin = date_fin

        # Remplacer par les fonctions qui génèrent les graphiques en fonction des dates sélectionnées
        st.session_state.html_code_1 = heatmap_collisions_filtree(date_debut, date_fin)
        st.session_state.html_code_2 = nuage_point_311(date_debut, date_fin)
        st.session_state.html_code_3 = heatmap_collisions_filtree(date_debut, date_fin)
        st.session_state.html_code_4 = heatmap_collisions_filtree(date_debut, date_fin)

        st.rerun()

# col1, col2 = st.columns(2)

# with col1:
with st.container():
    st.subheader("Heatmap des collisions")
    components.html(st.session_state.html_code_1, height=500)

# with col2:
with st.container():
    st.subheader("Nuage de points des requêtes 311")
    components.html(st.session_state.html_code_2, height=500)


# with col3:
with st.container():
    st.subheader("Graphique 3") #Titre a modifier
    components.html(st.session_state.html_code_3, height=500)

# with col4:
with st.container():
    st.subheader("Graphique 4") #Titre a modifier
    components.html(st.session_state.html_code_4, height=500)
