### build index from what is inside hash-embedding file
import sys
sys.path.append('/Users/qasem/PycharmProjects/lexitalk/')

# read the hash-embedding file
from core.embedding import EmbeddingManager

embedding_manager = EmbeddingManager()
hash_embeddings = embedding_manager.read_embeddings_from_file(
    embedding_manager.EMBEDDING_FILENAME_TXT)
print("Number of hash-embeddings in the file:", len(hash_embeddings))

# read all nodes from input_dir
from core.data_loader import DatasetReader

reader = DatasetReader(input_dir="data/raw/all")
reader.load_data()
text_nodes = reader.nodes

# take intersection of nodes hash and hash-embedding keys
embedded_nodes = [node for node in text_nodes if node.hash in hash_embeddings]

# prepare_data_and_embeddings for the intersection
from core.index_builder import prepare_data_and_embeddings, build_index
data_to_insert = prepare_data_and_embeddings(embedding_manager, 
                                             text_nodes=embedded_nodes)

print("Number of embedded nodes:", len(embedded_nodes))

# build_index for the intersection
from core.database import MongoDBClient
mongodb_client = MongoDBClient(database_name='default_db',
                                collection_name='default_collection',
                                index_name="vector_index")

# Sometimes insert_many fails, so we use insert_one
# mongodb_client.insert_many(data_to_insert)

from tqdm import tqdm

for datapoint in tqdm(data_to_insert[-30_000:]):
    try:
        mongodb_client.collection.insert_one(datapoint)
    except Exception as e:
        pass
