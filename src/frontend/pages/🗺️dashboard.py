import streamlit as st
from datetime import date

st.set_page_config(page_title=" Dashboard - Montréal", page_icon="🗺️", layout="wide")
st.title("🗺️ Dashboard - Montréal")

with st.sidebar:
    st.header("Période")

    date_debut = st.date_input(
        "Date de début",
        value=date(2026, 1, 1)  
    )

    date_fin = st.date_input(
        "Date de fin",
        value=date.today()  
    )

    is_valid_date = date_debut > date_fin
    if is_valid_date:
        st.error("La date de début doit être antérieure à la date de fin.")

    if st.button("Afficher les données", disabled=is_valid_date, width="stretch"):
        st.session_state.date_debut = date_debut
        st.session_state.date_fin = date_fin

        # fonction pour récupérer les données en fonction des dates a ajouter ici

        st.rerun()

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.subheader("Heatmap des collisions")  
        st.line_chart([1,2,3], height=200)

with col2:
    with st.container():
        st.subheader("Graphique 2") #Titre a modifier
        st.bar_chart([3,2,1], height=200)

col3, col4 = st.columns(2)

with col3:
    with st.container():
        st.subheader("Graphique 3") #Titre a modifier
        st.line_chart([1,2,3], height=200)

with col4:
    with st.container():
        st.subheader("Graphique 4") #Titre a modifier
        st.bar_chart([3,2,1], height=200)
