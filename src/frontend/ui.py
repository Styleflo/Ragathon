import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import uuid
from answer import ask

st.set_page_config(page_title="Mobility Copilot Montréal", layout="wide")
st.title("🚗 Mobility Copilot - Montréal")

if "conversations" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.conversations = {
        first_id: [{"role": "assistant", "content": "Que souhaitez-vous savoir ?"}]
    }
    st.session_state.current_conv_id = first_id

with st.sidebar:
    st.header("Historique des conversations")
    
    current_conv_messages = st.session_state.conversations[st.session_state.current_conv_id]
    is_current_empty = len([m for m in current_conv_messages if m["role"] == "user"]) == 0
    
    if st.button("➕ Nouvelle conversation", disabled=is_current_empty, width="stretch"):
        new_id = str(uuid.uuid4())
        st.session_state.conversations[new_id] = [{"role": "assistant", "content": "Que souhaitez-vous savoir ?"}]
        st.session_state.current_conv_id = new_id
        st.rerun()
    
    st.divider()

    conv_ids = list(st.session_state.conversations.keys())

    for conv_id in conv_ids:
        messages = st.session_state.conversations[conv_id]
        user_messages = [m["content"] for m in messages if m["role"] == "user"]
        title = user_messages[0][:20] + "..." if user_messages else "Nouvelle discussion"
        
        col1, col2 = st.columns([0.80, 0.20])
        
        with col1:
            is_active = (conv_id == st.session_state.current_conv_id)
            if st.button(title, key=f"select_{conv_id}", width="stretch", type="primary" if is_active else "secondary"):
                st.session_state.current_conv_id = conv_id
                st.rerun()
        
        with col2:
            can_delete = len(st.session_state.conversations) > 1
            if st.button("🗑️", key=f"del_{conv_id}", disabled=not can_delete, width="stretch"):
                del st.session_state.conversations[conv_id]
                
                if conv_id == st.session_state.current_conv_id:
                    st.session_state.current_conv_id = list(st.session_state.conversations.keys())[0]
                
                st.rerun()

response_container = st.container()

current_messages = st.session_state.conversations[st.session_state.current_conv_id]

with response_container:
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

user_query = st.chat_input("Posez votre question ici...")

if user_query:
    current_messages.append({"role": "user", "content": user_query})
    
    with response_container:
        with st.chat_message("user"):
            st.markdown(user_query)

    with st.spinner("Analyse en cours..."):
        # Get conversation history for context
        history = [(m["role"], m["content"]) for m in current_messages[:-1]]  # Exclude the just-added user message
        model_response = ask(user_query, history)
        
        current_messages.append({"role": "assistant", "content": model_response})
        
        st.rerun()


st.markdown("""
    <style>
    /* Couleur de fond du badge de l'ASSISTANT */
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #7B68EE !important; 
        color: white !important;
    }

    /* Couleur de fond du badge de l'USER */
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #262730 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)