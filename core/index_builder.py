from tqdm import tqdm

from llama_index.schema import MetadataMode
from llama_index.vector_stores.utils import node_to_metadata_dict

from core.data_loader import DatasetReader
from core.embedding import EmbeddingManager
from core.database import MongoDBClient
from core.utils import hash_node


def prepare_data_and_embeddings(
                embedding_manager: EmbeddingManager,
                input_dir=None,
                text_nodes=None,
                remove_text_in_metadata=True,
                remove_text_in_fields=False,
                ):
    """Prepares the data for insertion into the MongoDB collection.
    
    If text_nodes is not None, it will use that to prepare the data.
    Otherwise, it will use the input_dir to read the data.
    
    Generates or loads the embeddings for the text nodes.
    """
    assert (text_nodes is None) != (input_dir is None), "Either specify text_nodes or input_dir, not both"
    if text_nodes is None:
        reader = DatasetReader(input_dir=input_dir)
        reader.load_data()
        text_nodes = reader.nodes

    hash_embeddings = embedding_manager.load_or_generate_embeddings(text_nodes)

    data_to_insert = []
    for node in tqdm(text_nodes, desc="Pre-processing text nodes for MongoDB"):
        metadata = node_to_metadata_dict(node, remove_text=remove_text_in_metadata, flat_metadata=True)
        node_hash = hash_node(node)
        node_embedding = hash_embeddings[node_hash]
        entry = {
            "id": node.node_id,
            "metadata": metadata,
            "embedding": node_embedding,
            "hash": node_hash,
        }
        if not remove_text_in_fields:
            text = node.get_content(metadata_mode=MetadataMode.NONE) or ""
            entry["text"] = text
        
        data_to_insert.append(entry)
    return data_to_insert


def build_index(data_to_insert: list,
                mongodb_client: MongoDBClient,
                index_name="vector_index",
                ):
    mongodb_client.insert_many(data_to_insert)


if __name__ == "__main__":
    from core.database import MongoDBClient
    from core.embedding import EmbeddingManager

    mongodb_client = MongoDBClient(database_name='default_db',
                                   collection_name='default_collection',
                                   index_name="vector_index")

    embedding_manager = EmbeddingManager()
    
    data_to_insert = prepare_data_and_embeddings(embedding_manager, 
                                                 input_dir="data/raw/sample")
    
    build_index(data_to_insert, mongodb_client=mongodb_client)
