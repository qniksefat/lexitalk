import weaviate
import streamlit as st
import openai

from llama_index.vector_stores import WeaviateVectorStore
from llama_index import VectorStoreIndex, StorageContext

from core.data_loader import DatasetReader


def build_index(input_dir, index_name):
    weaviate_client = build_weaviate_client()
        
    reader = DatasetReader(input_dir=input_dir)
    reader.load_data()

    vector_store = WeaviateVectorStore(weaviate_client=weaviate_client, 
                                       index_name=index_name)
    
    # setting up the storage for the embeddings
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex(reader.nodes, 
                             storage_context=storage_context)
    
    return index


def build_weaviate_client():
    
    # maybe openai should be before storage_context?
    openai.api_key = st.secrets["openai_key"]

    auth_client_secret=weaviate.AuthApiKey(api_key=st.secrets["weaviate_key"])
    
    client = weaviate.Client(
            url=st.secrets["weaviate_url"],
            auth_client_secret=auth_client_secret,
            additional_headers={'X-OpenAI-Api-Key': st.secrets["openai_key"]})
            
    return client


def show_weaviate_schema(client):
    """This will show a list of classes/indexes in the weaviate instance."""
    import json
    
    schema = client.schema.get()
    print(json.dumps(schema, indent=2))


def delete_weaviate_index(client, index_name):
    """This will delete a class/index in the weaviate instance."""
    client.schema.delete_class(index_name)
    print(f"Deleted index {index_name}.")
