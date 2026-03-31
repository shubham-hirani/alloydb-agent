import streamlit as st
import os
from agent_logic import run_eco_agent

st.set_page_config(page_title="MambaMatrix: Eco-Matcher", page_icon="🌱")
st.title("🌱 Eco-Matcher Matchmaker")

supplier_id = st.sidebar.number_input("Enter Supplier ID", value=1)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about grant eligibility..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # The agent uses ADK to call the tool and generate a response
        response = run_eco_agent(prompt, supplier_id)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})