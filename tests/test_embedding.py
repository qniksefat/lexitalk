import os
import sys
sys.path.append('/Users/qasem/PycharmProjects/lexitalk/')

import unittest
from unittest.mock import MagicMock

from core.embedding import EmbeddingManager

class TestEmbeddingManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = EmbeddingManager(embedding_filename_txt="data/embedding/sample-embeddings.txt")
        self.mock_openai_client = MagicMock()
        self.manager.openai_client = self.mock_openai_client

    def test_get_embedding(self):
        # Mock response data
        mock_response = MagicMock()
        mock_response.data = [MagicMock(embedding=[0.1, 0.2, 0.3], text="test text")]
        self.mock_openai_client.embeddings.create.return_value = mock_response

        # Test get_embedding function
        embedding = self.manager.get_embedding("test text")
        self.assertEqual(embedding, [0.1, 0.2, 0.3])

    def test_read_embeddings_from_file(self):
        # Prepare a mock txt file
        with open("test_embedding_file.txt", "w") as f:
            f.write("hash_1: 0.1, 0.2, 0.3\nhash_2: 0.4, 0.5, 0.6\n")

        # Set the embedding filename to the mock file
        self.manager.embedding_filename_txt = "test_embedding_file.txt"

        # Test read_embeddings_from_file function
        embeddings = self.manager.read_embeddings_from_file()
        self.assertEqual(embeddings, {'hash_1': [0.1, 0.2, 0.3], 'hash_2': [0.4, 0.5, 0.6]})

    def test_write_embedding_to_file(self):
        # Prepare a mock txt file
        with open("test_embedding_file.txt", "w") as f:
            f.write("")

        # Set the embedding filename to the mock file
        self.manager.embedding_filename_txt = "test_embedding_file.txt"

        # Test write_embedding_to_file function
        self.manager.write_embedding_to_file("test_hash", [0.1, 0.2, 0.3])

        # Read the content of the mock file
        with open("test_embedding_file.txt", "r") as f:
            content = f.read()
        
        os.remove("test_embedding_file.txt")

        self.assertEqual(content, "test_hash: 0.1, 0.2, 0.3\n")

if __name__ == "__main__":
    unittest.main()
