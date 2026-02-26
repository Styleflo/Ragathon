import streamlit as st
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent.parent
SYNTHESIS_FILES = {
    "Grand public": FRONTEND_DIR / "synthesis_cache.md",
    "Municipalité": FRONTEND_DIR / "synthesis_cache_municipalite.md",
}

st.set_page_config(page_title="Tendances - Montréal", page_icon="📋", layout="wide")
st.title("📋 Synthèse - Montréal")

# Toggle switch
selected = st.radio(
    "Audience cible",
    options=list(SYNTHESIS_FILES.keys()),
    horizontal=True,
)

synthesis_file = SYNTHESIS_FILES[selected]

response_container = st.container()

with response_container:

    if synthesis_file.exists():
        content = synthesis_file.read_text(encoding="utf-8")
    else:
        content = f"⚠️ Synthèse '{selected}' non générée. Lancez `python generate_synthesis.py` pour la créer."

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