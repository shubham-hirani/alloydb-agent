import streamlit as st
import requests

st.title("🌱 Eco-Matcher Orchestrator")

tabs = st.tabs(["List New Item", "Chat with Agent"])

# Tab 1: Upload
with tabs[0]:
    st.header("List a Surplus Item")
    with st.form("list_form"):
        name = st.text_input("Your Name")
        title = st.text_input("Item Title")
        img = st.file_uploader("Upload Image", type=["jpg", "jpeg"])
        if st.form_submit_button("List Item"):
            files = {"image": img.getvalue()}
            data = {"provider_name": name, "item_title": title}
            res = requests.post("http://localhost:8000/api/list-item", data=data, files={"image": (img.name, img.getvalue())})
            st.success("Item Listed and Vectorized!")

# Tab 2: Chat
with tabs[1]:
    st.header("Find Resources")
    if prompt := st.chat_input("What are you looking for?"):
        with st.chat_message("user"): st.markdown(prompt)
        res = requests.post("http://localhost:8000/chat", json={
            "user_id": "demo", "session_id": "123", "message": prompt
        })
        with st.chat_message("assistant"): st.markdown(res.json()["response"])
