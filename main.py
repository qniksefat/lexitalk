import streamlit as st
import openai

from core.st_utils import (
    input_user_question, 
    display_chat_messages, 
    generate_assistant_response,
    initialize_chat_messages,
    make_sample_question_buttons,
)
from core.index_loader import load_vetor_index

openai.api_key = st.secrets.openai_key

st.set_page_config(
    page_title="LexiTalk",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": ("LexiTalk guides you through [Lex Fridman Podcast](https://lexfridman.com/podcast) "
                  "first 325 episodes taking transcripts from [here](https://karpathy.ai/lexicap/) unraveling perspectives.")

    },
)

st.title("Chat with Lex Fridman's Guests 💬")

index = load_vetor_index(index_name=st.secrets["weaviate_index_name"])

# Initialize the chat engine
if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = index.as_chat_engine(
        similarity_top_k=5,
        chat_mode="condense_question",
        verbose=True
    )

initialize_chat_messages()
st.write("\n")
make_sample_question_buttons()
input_user_question()
display_chat_messages(st.session_state.messages)

# If the last message is not from the assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    generate_assistant_response(
        st.session_state.chat_engine, st.session_state.messages[-1]["content"])
