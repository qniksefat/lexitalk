import weaviate
import streamlit as st
import openai 

from llama_index.vector_stores import WeaviateVectorStore
from llama_index import VectorStoreIndex


def load_vetor_index(index_name):
    openai.api_key = st.secrets["openai_key"]
    
    auth_client_secret=weaviate.AuthApiKey(api_key=st.secrets["weaviate_key"])
    
    client = weaviate.Client(
            url=st.secrets["weaviate_url"],
            auth_client_secret=auth_client_secret,
            additional_headers={'X-OpenAI-Api-Key': st.secrets["openai_key"]})
        
    # construct vector store
    vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name)

    loaded_index = VectorStoreIndex.from_vector_store(vector_store)
    return loaded_index
