import os
import openai
import streamlit as st
from tqdm import tqdm

from core.utils import hash_node
from core.config import EMBEDDING_FILENAME_TXT, EMBEDDING_MODEL_NAME

class EmbeddingManager:
    def __init__(self, embedding_filename_txt=None, embedding_model_name=None, api_key=None):
        if embedding_filename_txt:
            if not embedding_filename_txt.endswith(".txt"):
                raise ValueError("Embedding filename should end with .txt")
            if not os.path.exists(embedding_filename_txt):
                raise ValueError(f"Embedding filename {embedding_filename_txt} does not exist.")
            self.embedding_filename_txt = embedding_filename_txt
        else:
            self.embedding_filename_txt = EMBEDDING_FILENAME_TXT
        
        self.embedding_model_name = embedding_model_name or EMBEDDING_MODEL_NAME
        self.api_key = api_key or st.secrets.get("openai_key")
        if not self.api_key:
            raise ValueError("OpenAI API key is missing.")

        self.openai_client = openai.Client(api_key=self.api_key)

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        embed = self.openai_client.embeddings
        response = embed.create(input=[text], model=self.embedding_model_name)
        return response.data[0].embedding

    def read_embeddings_from_file(self) -> dict:
        """Reads embeddings from a txt file and returns a dictionary of embeddings.

        The node hash values might be repeated in the txt file, in which case the last
        value will be used.

        The txt file should have the following format:
        ```
        node_hash_1: 0.1, 0.2, 0.3, ...
        ```
        """            
        with open(self.embedding_filename_txt, "r") as f:
            lines = f.readlines()
        embeddings = {}
        for line in lines:
            key, value = line.split(": ")
            embeddings[key] = list(map(float, value.split(", ")))
        return embeddings

    def write_embedding_to_file(self, node_hash: str, embedding: list):
        """Writes a single embedding to a txt file."""
        with open(self.embedding_filename_txt, "a") as f:
            f.write(f"{node_hash}: {', '.join(map(str, embedding))}\n")

    def load_or_generate_embeddings(self, nodes) -> dict:
        embedding_filename = self.embedding_filename_txt
        hash_embeddings = self.read_embeddings_from_file()

        for node in tqdm(nodes, desc="Loading or generating embeddings"):
            node_hash = hash_node(node)
            if node_hash not in hash_embeddings:
                node_embedding = self.get_embedding(node.text)
                hash_embeddings[node_hash] = node_embedding
                self.write_embedding_to_file(node_hash, node_embedding)

        return hash_embeddings
