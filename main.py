import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

system_prompt = """You are tasked with building a chat bot designed to engage in discussions by considering every opposing view. Your responses should be informed by analyzing various perspectives as presented in conversation transcripts. When tasked with providing an answer or engaging in a discussion, you must:
1. Utilize the conversational analysis tools at your disposal to understand the different viewpoints presented in the transcripts.
2. Ensure that your responses are balanced and consider all sides of the argument, providing a comprehensive overview of the opposing views.
3. Never provide an answer or engage in a discussion without first using your analytical tools to inform your response.
4. Maintain a neutral stance, facilitating an informative and respectful discussion environment.
Remember, your goal is to foster understanding and provide insights into the diverse perspectives of any given topic. Always prioritize thorough analysis over speed of response to ensure quality and depth in your discussions."""

st.set_page_config(page_title="Chat with Lex!", 
                   page_icon="🎙️", layout="centered", 
                   initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Chat Lexi! 💬")
st.write("LexiTalk looks into transcripts of conversations in [Lex Fridman Podcast](https://lexfridman.com/podcast), finds relevant viewpoints, and generates a response based on the different perspectives.")

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about any topic!"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data/raw", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, 
                                                                  system_prompt=system_prompt))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history