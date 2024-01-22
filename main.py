import streamlit as st
import openai
openai.api_key = st.secrets.openai_key

from core.index_loader import load_vetor_index
from core.st_utils import display_sources

st.set_page_config(page_title="Chat with Lex!", 
                   page_icon="🎙️", layout="centered", 
                   initial_sidebar_state="auto", menu_items=None)
st.title("Chat Lexi! 💬")
st.write("LexiTalk looks into transcripts of conversations in [Lex Fridman Podcast](https://lexfridman.com/podcast), finds relevant viewpoints, and generates a response based on the different perspectives.")

# Initialize the chat messages history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me about any topic!"}
    ]

index = load_vetor_index(index_name="Lexi1")

# Initialize the chat engine
if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display the prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            display_sources(response.source_nodes)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
