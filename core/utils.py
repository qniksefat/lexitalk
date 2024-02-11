from typing import List
from llama_index import Document
from llama_index.schema import Node

from hashlib import sha256


def hash_list_docs(docs: List[Document]):
    if any(not isinstance(doc, Document) for doc in docs):
        raise TypeError("custom_hash_function only works with Document objects")
    docs.sort(key=lambda doc: doc.hash)
    hashable_info_list = [doc.hash for doc in docs]
    combined_info = ",".join(map(str, hashable_info_list))
    hash_value = sha256(combined_info.encode()).hexdigest()
    return hash_value


def hash_node(node: Node) -> str:
    """Generate a hash to represent the node."""
    values = node.__dict__.copy()
    text = values.get("text", "")
    metadata = values.get("metadata", {})
    doc_identity = str(text) + str(metadata)
    return str(
        sha256(doc_identity.encode("utf-8", "surrogatepass")).hexdigest()
    )
