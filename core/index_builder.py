import weaviate
import streamlit as st
import openai

from llama_index.vector_stores import WeaviateVectorStore
from llama_index import VectorStoreIndex, StorageContext

from core.data_loader import load_nodes


def build_index(input_dir, index_name):
    client = weaviate.Client(
        embedded_options=weaviate.embedded.EmbeddedOptions(),
        additional_headers={'X-OpenAI-Api-Key': st.secrets["openai_key"]})
    
    nodes = load_nodes(input_dir)

    vector_store = WeaviateVectorStore(weaviate_client=client, index_name=index_name)

    openai.api_key = st.secrets["openai_key"]
    
    # setting up the storage for the embeddings
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex(nodes, storage_context=storage_context)

    return index
