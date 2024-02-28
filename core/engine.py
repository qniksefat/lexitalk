import streamlit as st

from llama_index import ServiceContext, VectorStoreIndex
from llama_index.vector_stores import MongoDBAtlasVectorSearch
from llama_index.embeddings import OpenAIEmbedding
from llama_index.llms import OpenAI
from llama_index.postprocessor.cohere_rerank import CohereRerank

from core.database import MongoDBClient
from core.embedding import EmbeddingManager
from core.config import (
    LLM_SYSTEM_PROMPT, 
    LLM_MODEL_NAME, 
    LLM_TEMPERATURE,
    NUM_RETRIEVED_DOCS,
    NUM_DOCUMENTS_TO_LLM,
)


def build_chat_engine(use_rerank: bool = False):
    
    mongodb_client = MongoDBClient()
    vector_store = MongoDBAtlasVectorSearch(mongodb_client=mongodb_client.client, 
                                            index_name=mongodb_client.index_name)
    
    
    embedding_manager = EmbeddingManager()
    embed_model = OpenAIEmbedding(
            model_name=embedding_manager.embedding_model_name,
            api_key=st.secrets["openai_key"])
    
    llm = OpenAI(
        model=LLM_MODEL_NAME,
        system_prompt=LLM_SYSTEM_PROMPT,
        temperature=LLM_TEMPERATURE,
        api_key=st.secrets["openai_key"])

    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    
    
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store,
                                               service_context=service_context)
    
    reranker = CohereRerank(api_key=st.secrets["cohere_key"], 
                                 top_n=NUM_DOCUMENTS_TO_LLM)
    

    node_postprocessors = []
    if use_rerank:
        reranker = CohereRerank(api_key=st.secrets["cohere_key"], 
                                    top_n=NUM_DOCUMENTS_TO_LLM)
        node_postprocessors.append(reranker)

    chat_engine = index.as_chat_engine(
        similarity_top_k=NUM_RETRIEVED_DOCS,
        node_postprocessors=node_postprocessors,
        chat_mode="condense_question",
        verbose=True,
    )
    
    return chat_engine
