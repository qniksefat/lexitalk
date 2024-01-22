from typing import List, Dict
import os

from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser

from core.config import INPUT_DIR


class DatasetReader:
    def __init__(self, input_dir=INPUT_DIR):
        self.input_dir = input_dir
        self.docs = None
        self.nodes = None

    def load_documents(self):
        """Load data from the specified directory."""
        reader = SimpleDirectoryReader(input_dir=self.input_dir, 
                                       file_metadata=self.metadata_extractor)
        self.docs = reader.load_data()

    def fill_documents(self):
        """Fill in the documents attribute."""
        if not self.docs:
            raise ValueError("Documents have not been loaded. Call load_data first.")
        # Your document processing logic goes here

    def fill_nodes(self):
        """Fill in the nodes attribute."""
        if not self.docs:
            raise ValueError("Documents have not been loaded. Call load_data first.")
        
        parser = SimpleNodeParser.from_defaults(
            chunk_size=512,
            chunk_overlap=128,
            include_metadata=True,
            include_prev_next_rel=True,
        )
        self.nodes = parser.get_nodes_from_documents(self.docs)

    def load_data(self):
        """Load data, fill documents, and fill nodes."""
        self.load_documents()
        self.fill_documents()
        self.fill_nodes()
    
    @staticmethod
    def metadata_extractor(file_path: str) -> Dict:
        """Get some handy metadate from filesystem.

        Args:
            file_path: str: file path in str
        """
        file_name = os.path.basename(file_path)
        return {
            "file_path": file_path,
            "file_name": file_name,
            "file_type": file_name.split(".")[-1],
            "file_size": os.path.getsize(file_path),
            "episode_number": int(file_name.split("_")[1])
        }


if __name__ == "__main__":
    # Example of using EpisodeReader
    episode_reader = DatasetReader()
    episode_reader.load_data()

    # Access documents and nodes attributes if needed
    documents = episode_reader.docs
    nodes = episode_reader.nodes
