import streamlit as st
from datetime import date
import streamlit.components.v1 as components

st.set_page_config(page_title=" Dashboard - Montréal", page_icon="🗺️", layout="wide")
st.title("🗺️ Dashboard - Montréal")

with st.sidebar:
    st.header("Période")

    date_debut = st.date_input("Date de début", value=date(2026, 1, 1))
    date_fin = st.date_input("Date de fin", value=date.today())


    # Remplacer par les fonctions qui génèrent les graphiques en fonction des dates sélectionnées
    if "html_code_1" not in st.session_state:
        st.session_state.html_code_1 = """ fonction(date_debut, date_fin) """
        st.session_state.html_code_2 = """ fonction(date_debut, date_fin) """
        st.session_state.html_code_3 = """ fonction(date_debut, date_fin) """
        st.session_state.html_code_4 = """ fonction(date_debut, date_fin) """

    is_valid_date = date_debut > date_fin
    if is_valid_date:
        st.error("La date de début doit être antérieure à la date de fin.")

    if st.button("Afficher les données", disabled=is_valid_date, width="stretch"):
        st.session_state.date_debut = date_debut
        st.session_state.date_fin = date_fin

        # Remplacer par les fonctions qui génèrent les graphiques en fonction des dates sélectionnées
        st.session_state.html_code_1 = """ fonction(date_debut, date_fin) """
        st.session_state.html_code_2 = """ fonction(date_debut, date_fin) """
        st.session_state.html_code_3 = """ fonction(date_debut, date_fin) """
        st.session_state.html_code_4 = """ fonction(date_debut, date_fin) """

        st.rerun()

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.subheader("Heatmap des collisions")  
        components.html(st.session_state.html_code_1, height=200)  

with col2:
    with st.container():
        st.subheader("Graphique 2") #Titre a modifier
        components.html(st.session_state.html_code_2, height=200)

col3, col4 = st.columns(2)

with col3:
    with st.container():
        st.subheader("Graphique 3") #Titre a modifier
        components.html(st.session_state.html_code_3, height=200)

with col4:
    with st.container():
        st.subheader("Graphique 4") #Titre a modifier
        components.html(st.session_state.html_code_4, height=200)
