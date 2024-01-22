from typing import List
from llama_index import Document
from hashlib import sha256


def hash_list_docs(docs: List[Document]):
    if any(not isinstance(doc, Document) for doc in docs):
        raise TypeError("custom_hash_function only works with Document objects")
    docs.sort(key=lambda doc: doc.hash)
    hashable_info_list = [doc.hash for doc in docs]
    combined_info = ",".join(map(str, hashable_info_list))
    hash_value = sha256(combined_info.encode()).hexdigest()
    return hash_value
