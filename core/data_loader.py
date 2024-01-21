from core.config import SYSTEM_PROMPT, INPUT_DIR


import streamlit as st
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import OpenAI


@st.cache_resource(show_spinner=True)
def load_vetor_index():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take a few minutes."):
        reader = SimpleDirectoryReader(
            input_dir=INPUT_DIR,
            recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo",
                                                                  temperature=0.5,
                                                                  system_prompt=SYSTEM_PROMPT))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index