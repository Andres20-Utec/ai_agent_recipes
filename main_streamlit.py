import streamlit as st
from backend.core import run_llm
from streamlit_chat import message

st.header("Peruvian Chef Bot")

# Initialize chat history
if (
    "user_messages" not in st.session_state
    and "chat_history" not in st.session_state
    and "ai_answer" not in st.session_state
):
    st.session_state["user_messages"] = []
    st.session_state["ai_answer"] = []
    st.session_state["chat_history"] = []

# Sidebar
st.sidebar.title("Parameters")
temperature = st.sidebar.slider(
    "Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01
)
max_tokens = st.sidebar.slider(
    "Max tokens", min_value=50, max_value=16384, value=1800, step=50
)

prompt = st.chat_input("Write a question ..")

if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        formatted_response = generated_response["result"]
        st.session_state["ai_answer"].append(formatted_response)
        st.session_state["user_messages"].append(prompt)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", formatted_response))

if st.session_state["chat_history"]:
    for user_message, ai_message in zip(
        st.session_state["user_messages"], st.session_state["ai_answer"]
    ):
        message(user_message, is_user=True)
        message(ai_message)
