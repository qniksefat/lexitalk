from typing import List, Dict
import os
import re

from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser

from core.metadata import metadata_yt


class DatasetReader:
    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.docs = None
        self.nodes = None

    def load_documents(self):
        """Load data from the specified directory."""
        reader = SimpleDirectoryReader(input_dir=self.input_dir, 
                                       file_metadata=self.metadata_extractor_from_filename)
        self.docs = reader.load_data()

    def fill_documents(self):
        """Fill in the documents attribute."""
        if not self.docs:
            raise ValueError("Documents have not been loaded. Call load_data first.")
        
        # Your document processing logic goes here        
        for doc in self.docs:
            if doc.text.startswith("WEBVTT"):
                doc.text = doc.text[len("WEBVTT"):]
            self.append_metadata_doc_yt_info(doc)

    def fill_nodes(self):
        """Fill in the nodes attribute."""
        if not self.docs:
            raise ValueError("Documents have not been loaded. Call load_data first.")
        
        parser = EpisodeTextSplitter.from_defaults(
            chunk_size=512,
            chunk_overlap=128,
            include_metadata=True,
            include_prev_next_rel=True,
        )
        self.nodes = parser.get_nodes_from_documents(self.docs)
        self.nodes = append_metadata_nodes_timestamps(self.nodes)

    def load_data(self):
        """Load data, fill documents, and fill nodes."""
        self.load_documents()
        self.fill_documents()
        self.fill_nodes()
    
    @staticmethod
    def metadata_extractor_from_filename(file_path: str) -> Dict:
        """Get some handy metadate from filesystem.

        Args:
            file_path: str: file path in str
        """
        file_name = os.path.basename(file_path)
        return {
            "file_path": file_path,
            "file_name": file_name,
            "file_type": file_name.split(".")[-1],
            "file_size": str(os.path.getsize(file_path)),
            # this will remove leading zeros from the episode number
            "episode_number": str(int(file_name.split("_")[1]))
        }
        
    def append_metadata_doc_yt_info(self, doc):
        """Append metadata from youtube info dataframe to the document."""
        # for every column in the dataframe, append the value to the document.metadata
        for column in metadata_yt.columns:
            doc.metadata[column] = metadata_yt.loc[doc.metadata["episode_number"], column]


class EpisodeTextSplitter(SimpleNodeParser):
    def _postprocess_chunks(self, chunks: List[str]) -> List[str]:
        """Post-process chunks for custom requirements."""
        processed_chunks: List[str] = []

        for chunk in chunks:
            # Find the first timestamp in the chunk
            match = re.search(r'\d{1,2}:\d{2}(:\d{2})?\.\d{3}', chunk)
            first_timestamp = match.group(0) if match else "NA"

            # Remove unnecessary timestamps from the text
            chunk_without_timestamps = re.sub(r'\d{1,2}:\d{2}(:\d{2})?\.\d{3}', '', chunk)

            # Remove extra new lines
            cleaned_chunk = ' '.join(line.strip() 
                                     for line in chunk_without_timestamps.split('\n') 
                                     if line.strip())
            cleaned_chunk = cleaned_chunk.replace("-->", "")
            cleaned_chunk = cleaned_chunk.replace("  ", " ")
            cleaned_chunk = cleaned_chunk.strip()

            # Append the first timestamp on a new line at the beginning of the chunk
            cleaned_chunk = f"{first_timestamp}\n{cleaned_chunk}"
            processed_chunks.append(cleaned_chunk)
        return processed_chunks


def append_metadata_nodes_timestamps(nodes):
    """Append timestamp metadata to each node."""
    for node in nodes:
        node.metadata["timestamp"]: str = node.text.split("\n")[0]
        node.text = "\n".join(node.text.split("\n")[1:])
    return nodes


if __name__ == "__main__":
    # Example of using EpisodeReader
    episode_reader = DatasetReader("data/raw/sample/")
    episode_reader.load_data()

    # Access documents and nodes attributes if needed
    documents = episode_reader.docs
    nodes = episode_reader.nodes
