from tqdm import tqdm

from llama_index.schema import MetadataMode
from llama_index.vector_stores.utils import node_to_metadata_dict

from core.data_loader import DatasetReader
from core.embedding import load_or_generate_embeddings
from core.utils import hash_node


def build_index(input_dir, 
                mongodb_client, 
                openai_client, 
                index_name="vector_index",
                remove_text=True    # Already saving text in node_content along with metadata
                ):
    reader = DatasetReader(input_dir=input_dir)
    reader.load_data()

    hash_embeddings = load_or_generate_embeddings(reader.nodes, openai_client)

    data_to_insert = []
    for node in tqdm(reader.nodes, desc="Pre-processing text nodes for MongoDB"):
        metadata = node_to_metadata_dict(node, remove_text=remove_text, flat_metadata=True)
        node_hash = hash_node(node)
        node_embedding = hash_embeddings[node_hash]
        entry = {
            "id": node.node_id,
            "metadata": metadata,
            "embedding": node_embedding,
            "hash": node_hash,
        }
        
        if not remove_text:
            text = node.get_content(metadata_mode=MetadataMode.NONE) or ""
            entry["text"] = text
        
        data_to_insert.append(entry)

    mongodb_client.insert_many(data_to_insert)


if __name__ == "__main__":
    from core.database import MongoDBClient
    from core.embedding import OpenAIClient

    mongodb_client = MongoDBClient(database_name='default_db',
                                   collection_name='default_collection',
                                   index_name="vector_index")

    openai_client = OpenAIClient()

    build_index(input_dir="data/raw/sample",
                mongodb_client=mongodb_client,
                openai_client=openai_client)
