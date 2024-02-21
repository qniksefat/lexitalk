import streamlit as st

from core.st_utils import (
    input_user_question, 
    display_chat_messages, 
    generate_assistant_response,
    initialize_chat_messages,
    make_sample_question_buttons,
)
from core.index_loader import build_chat_engine

st.set_page_config(
    page_title="LexChat 💦 💬",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": "This is a Streamlit app for conversing with Lex Fridman's guests.",
        "Report a bug": "https://github.com/qniksefat/lexitalk/issues/new",
        "Get help": "https://github.com/qniksefat/lexitalk/",
    },
)

st.title("Chat with Lex Fridman's Guests 💬")

st.info("Welcome aboard our AI-driven magic carpet! Journey through the fascinating depths"
        " of minds from Lex Fridman Podcast [(link)](https://lexfridman.com/podcast). Decide YOUR"
        " sources of truth. No reading required—just click and listen from the moment of discussion!",
        icon="💡")

# Initialize the chat engine
if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = build_chat_engine()

initialize_chat_messages()
st.write("\n")
make_sample_question_buttons()
input_user_question()
display_chat_messages(st.session_state.messages)

# If the last message is not from the assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    generate_assistant_response(
        st.session_state.chat_engine, st.session_state.messages[-1]["content"])
