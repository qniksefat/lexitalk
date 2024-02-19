import streamlit as st

from llama_index import ServiceContext, VectorStoreIndex
from llama_index.vector_stores import MongoDBAtlasVectorSearch
from llama_index.embeddings import OpenAIEmbedding
from llama_index.llms import OpenAI

from core.database import MongoDBClient
from core.embedding import EmbeddingManager
from core.config import SYSTEM_PROMPT


def load_vetor_index(index_name):
    mongodb_client = MongoDBClient(database_name='default_db',
                                   collection_name='default_collection',
                                   index_name=index_name)
    
    # construct vector store
    vector_store = MongoDBAtlasVectorSearch(mongodb_client=mongodb_client.client, 
                                            index_name=mongodb_client.index_name)
    
    # Specify the Embedding model (and LLM model) in a ServiceContext
    openai_client = EmbeddingManager()
    
    embed_model = OpenAIEmbedding(
            model_name=openai_client.EMBEDDING_MODEL_NAME,
            api_key=st.secrets["openai_key"])
    
    llm = OpenAI(model="gpt-3.5-turbo",
             system_prompt=SYSTEM_PROMPT,
             api_key=st.secrets["openai_key"])

    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

    loaded_index = VectorStoreIndex.from_vector_store(vector_store=vector_store,
                                                      service_context=service_context)

    return loaded_index
