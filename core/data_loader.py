from core.config import INPUT_DIR

from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser


class EpisodeReader:
    def __init__(self, input_dir=INPUT_DIR):
        self.input_dir = input_dir
        self.docs = None
        self.nodes = None

    def load_documents(self):
        """Load data from the specified directory."""
        reader = SimpleDirectoryReader(input_dir=self.input_dir, recursive=True)
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
            include_metadata=True,
            include_prev_next_rel=True,
        )
        self.nodes = parser.get_nodes_from_documents(self.docs)

    def load_data(self):
        """Load data, fill documents, and fill nodes."""
        self.load_documents()
        self.fill_documents()
        self.fill_nodes()


if __name__ == "__main__":
    # Example of using EpisodeReader
    episode_reader = EpisodeReader()
    episode_reader.load_data()

    # Access documents and nodes attributes if needed
    documents = episode_reader.docs
    nodes = episode_reader.nodes
