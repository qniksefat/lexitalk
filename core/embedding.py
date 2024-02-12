import os
import json
import openai
import streamlit as st
from tqdm import tqdm

from core.utils import hash_node

EMBEDDING_FILENAME = "data/embedding/hash-node-to-embedding-model=openai-3-small.json"


class OpenAIClient:
    EMBEDDING_MODEL_NAME = "text-embedding-3-small"

    def __init__(self, api_key=st.secrets["openai_key"]):
        self.openai_client = openai.Client(api_key=api_key)

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        embed = self.openai_client.embeddings
        response = embed.create(input=[text], model=self.EMBEDDING_MODEL_NAME)
        return response.data[0].embedding


def load_or_generate_embeddings(nodes, 
                                openai_client, 
                                embedding_filename=EMBEDDING_FILENAME):

    if os.path.exists(embedding_filename):
        with open(embedding_filename, "r") as f:
            hash_embeddings = json.load(f)
    else:
        hash_embeddings = {}

    for node in tqdm(nodes, desc="Loading/generating embeddings"):
        node_hash = hash_node(node)
        if node_hash not in hash_embeddings:
            hash_embeddings[node_hash] = openai_client.get_embedding(node.text)

    with open(embedding_filename, "w") as f:
        json.dump(hash_embeddings, f)

    return hash_embeddings
