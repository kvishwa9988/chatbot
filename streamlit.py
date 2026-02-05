import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Cyber Secuirty Chatbot")

st.title("🤖 Cyber Security AI Assistant")
st.markdown("---")

# 1. Initialize Session IDs and Chat History
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. Chat Input
if prompt := st.chat_input("Ask.."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. Request to FastAPI Backend
    with st.spinner("Thinking..."):
        try:
            payload = {
                "message": prompt,
                "session_id": st.session_state.session_id
            }
            response = requests.post("https://chatbot-1-6wzd.onrender.com/", json=payload)
            
            if response.status_code == 200:
                bot_response = response.json()["output"]
                
                # Add bot message to UI
                with st.chat_message("assistant"):
                    st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:

            st.error(f"Failed to connect to backend: {e}")
