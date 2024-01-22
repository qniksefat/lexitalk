from core.config import INPUT_DIR

from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser

def load_docs(input_dir=INPUT_DIR):
    reader = SimpleDirectoryReader(
        input_dir=input_dir,
        recursive=True)
    docs = reader.load_data()
    return docs

def extract_nodes(docs):
    parser = SimpleNodeParser.from_defaults(
        chunk_size=512,
        include_metadata=True,
        include_prev_next_rel=True,
    )
    nodes = parser.get_nodes_from_documents(docs)
    return nodes

def load_nodes(input_dir=INPUT_DIR):
    docs = load_docs(input_dir)
    nodes = extract_nodes(docs)
    return nodes
