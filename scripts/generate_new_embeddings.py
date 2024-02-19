import sys
sys.path.append('/Users/qasem/PycharmProjects/lexitalk/')

from core.data_loader import DatasetReader
from core.embedding import EmbeddingManager

reader = DatasetReader(input_dir="data/raw/all/")
reader.load_data()
text_nodes = reader.nodes

embedding_manager = EmbeddingManager()

hash_embeddings = embedding_manager.load_or_generate_embeddings(text_nodes[::-1])
