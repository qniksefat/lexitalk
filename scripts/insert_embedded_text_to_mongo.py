"""insert documents concurrently to mongodb from text nodes that have embeddings in file
"""
import sys
sys.path.append('/Users/qasem/PycharmProjects/lexitalk/')

# get the hash-embedding filename
def get_hash_embedding_filename():
    from os.path import join
    dir = "/Users/qasem/PycharmProjects/git-changes--should then stash pop"
    fname = "hash-node-to-embedding-model=openai-3-small 2.txt"
    return join(dir, fname)

EMBEDDING_FILENAME = get_hash_embedding_filename()
INPUT_TEXT_DIR = "data/raw/all"



# read the hash-embedding file
from core.embedding import EmbeddingManager

embedding_manager = EmbeddingManager(
    embedding_filename_txt=EMBEDDING_FILENAME)

hash_embeddings = embedding_manager.read_embeddings_from_file()
print("Number of hash-embeddings in the file:", len(hash_embeddings))

# read all nodes from input_dir
from core.data_loader import DatasetReader

reader = DatasetReader(input_dir=INPUT_TEXT_DIR)
reader.load_data()
text_nodes = reader.nodes

# take intersection of nodes hash and hash-embedding keys
embedded_nodes = [node for node in text_nodes if node.hash in hash_embeddings]

# prepare_data_and_embeddings for the intersection
from core.index_builder import prepare_data_and_embeddings
data_to_insert = prepare_data_and_embeddings(embedding_manager, 
                                             text_nodes=embedded_nodes)

print("Number of embedded nodes:", len(embedded_nodes))

# build_index for the intersection
from core.database import MongoDBClient
mongodb_client = MongoDBClient(database_name='default_db',
                                collection_name='default_collection',
                                index_name="vector_index")



# if hash is not an index, create it
if "hash_1" not in mongodb_client.collection.index_information():
    mongodb_client.collection.create_index([("hash", 1)], unique=True)


def insert_data_into_mongodb_if_not_exists(data_entry, mongodb_client):
    """Inserts the data entry into the MongoDB collection if it does not exist.
    """
    hash = data_entry["hash"]
    if not mongodb_client.collection.find_one({"hash": hash}):
        mongodb_client.collection.insert_one(data_entry)
        print(f"Node {hash} inserted successfully")
    else:
        print(f"Node {hash} already exists in the collection")
    return hash


from concurrent.futures import ThreadPoolExecutor, as_completed

def insert_data_into_mongodb_concurrently(data_to_insert, mongodb_client, num_workers):
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_hash = {
            executor.submit(insert_data_into_mongodb_if_not_exists, data_entry, mongodb_client): 
            data_entry["hash"] for data_entry in data_to_insert
            }
        
        for future in as_completed(future_to_hash):
            hash = future_to_hash[future]
            try:
                data = future.result()
            except Exception as exc:
                print(f'Node {hash} generated an exception: {exc}')
            else:
                pass

insert_data_into_mongodb_concurrently(data_to_insert, mongodb_client, num_workers=10)
