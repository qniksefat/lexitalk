import os
import openai
import streamlit as st
from tqdm import tqdm

from core.utils import hash_node


class EmbeddingManager:
    """Manages the embeddings for the text nodes.
    It can read embeddings from a txt file, generate embeddings using OpenAI's API,
    """
    EMBEDDING_FILENAME_TXT = "data/embedding/hash-node-to-embedding-model=openai-3-small.txt"
    EMBEDDING_MODEL_NAME = "text-embedding-3-small"

    def __init__(self, api_key=st.secrets["openai_key"]):
        self.openai_client = openai.Client(api_key=api_key)

    def get_embedding(self, text):
        text = text.replace("\n", " ")
        embed = self.openai_client.embeddings
        response = embed.create(input=[text], model=self.EMBEDDING_MODEL_NAME)
        return response.data[0].embedding

    def read_embeddings_from_file(self, embedding_filename_txt: str) -> dict:
        """Reads embeddings from a txt file and returns a dictionary of embeddings.

        The node hash values might be repeated in the txt file, in which case the last
        value will be used.

        The txt file should have the following format:
        ```
        node_hash_1: 0.1, 0.2, 0.3, ...
        ```
        """
        if not os.path.exists(embedding_filename_txt):
            return {}

        assert embedding_filename_txt.endswith(".txt"), "The file should be a txt file."

        with open(embedding_filename_txt, "r") as f:
            lines = f.readlines()
        embeddings = {}
        for line in lines:
            key, value = line.split(": ")
            embeddings[key] = list(map(float, value.split(", ")))
        return embeddings

    def write_embedding_to_file(self, embedding_filename_txt: str, 
                                node_hash: str, embedding: list):
        """Writes a single embedding to a txt file."""
        with open(embedding_filename_txt, "a") as f:
            f.write(f"{node_hash}: {', '.join(map(str, embedding))}\n")

    def load_or_generate_embeddings(self, nodes) -> dict:
        embedding_filename = self.EMBEDDING_FILENAME_TXT
        hash_embeddings = self.read_embeddings_from_file(embedding_filename)

        for node in tqdm(nodes, desc="Loading or generating embeddings"):
            node_hash = hash_node(node)
            if node_hash not in hash_embeddings:
                node_embedding = self.get_embedding(node.text)
                hash_embeddings[node_hash] = node_embedding
                self.write_embedding_to_file(embedding_filename, 
                                             node_hash, node_embedding)

        return hash_embeddings
