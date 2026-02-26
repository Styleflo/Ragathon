import streamlit as st

st.set_page_config(page_title="Tendances - Montréal", page_icon="📋", layout="wide")
st.title("📋 Synthèse - Montréal")

response_container = st.container()

with response_container:

    content = """ Réponse à venir... """

    with st.chat_message("assistant"):
        st.markdown(content)

st.markdown("""
    <style>
    /* Couleur de fond du badge de l'ASSISTANT */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #7B68EE !important; 
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)