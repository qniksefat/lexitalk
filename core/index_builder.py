import weaviate
import streamlit as st
import openai

from llama_index.vector_stores import WeaviateVectorStore
from llama_index import VectorStoreIndex, StorageContext

from core.data_loader import EpisodeReader


def build_index(input_dir, index_name):

    auth_client_secret=weaviate.AuthApiKey(api_key=st.secrets["weaviate_key"])
    
    client = weaviate.Client(
            url=st.secrets["weaviate_url"],
            auth_client_secret=auth_client_secret,
            additional_headers={'X-OpenAI-Api-Key': st.secrets["openai_key"]})
        
    reader = EpisodeReader(input_dir=input_dir)
    reader.load_data()
    nodes = reader.nodes

    vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name)

    openai.api_key = st.secrets["openai_key"]
    
    # setting up the storage for the embeddings
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    return index