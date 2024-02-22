from datetime import datetime, timedelta
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


def parse_timestamp(timestamp_str: str) -> datetime:
    """Parses a timestamp string with or without milliseconds or hours into a datetime object.
    """
    if "." in timestamp_str:
        # Has milliseconds in the end
        if len(timestamp_str.split(":")) == 3:
            # Has hours in the beginning
            timestamp = datetime.strptime(timestamp_str, '%H:%M:%S.%f')
        else:
            timestamp = datetime.strptime(timestamp_str, '%M:%S.%f')
    else:
        if len(timestamp_str.split(":")) == 3:
            timestamp = datetime.strptime(timestamp_str, '%H:%M:%S')
        else:
            timestamp = datetime.strptime(timestamp_str, '%M:%S')
    return timestamp.time()     # No date is in the range of of a video


def convert_timestamp_str_to_seconds(timestamp_str: str) -> int:
    """Converts a timestamp string to number of total seconds.

    Returns:
        int: Number of seconds.
    """
    timestamp = parse_timestamp(timestamp_str)
    seconds = timedelta(
        hours=timestamp.hour,
        minutes=timestamp.minute,
        seconds=timestamp.second,
        microseconds=timestamp.microsecond).total_seconds()
    return int(seconds)
