import streamlit as st
import time
from inference import engine

# Page config
st.set_page_config(
    page_title="NicheForge",
    page_icon="⚒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ... (styles remain same)

# --- MAIN CONTENT ---
col1, col2 = st.columns([1, 4])

# Center content slightly
with col2:
    st.title("NicheForge")
    st.markdown("### The Domain-Specific AI Builder")
    st.markdown("ask anything about **Polars**, or train it on your own docs.")

st.divider()

# Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcome message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": f"Hello! I'm connected to **{engine.active_backend.upper()}**. Ask me anything about DataFrames, Expressions, or Lazy performance."
    })

# Render Chat
for message in st.session_state.messages:
    role = message["role"]
    avatar = "👤" if role == "user" else "📚"
    
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

# Input Area
if prompt := st.chat_input("How do I filter rows in Polars?"):
    # Render User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Render Bot Response
    with st.chat_message("assistant", avatar="📚"):
        message_placeholder = st.empty()
        
        # simulated typing effect
        with st.spinner("Processing..."):
            try:
                full_response = engine.generate(prompt, temperature=st.session_state.temp)
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Error: {e}")
                full_response = "I encountered an error generating the response."
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
