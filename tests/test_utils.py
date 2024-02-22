import sys
sys.path.append('/Users/qasem/PycharmProjects/lexitalk/')
from datetime import time
import unittest

from core.utils import (
    Node, Document,
    parse_timestamp,
    convert_timestamp_str_to_seconds,
    hash_list_docs,
    hash_node,
)


class TestUtils(unittest.TestCase):
    
    def test_convert_timestamp_str_to_seconds(self):
        self.assertEqual(convert_timestamp_str_to_seconds("0:0:0.000"), 0)
        self.assertEqual(convert_timestamp_str_to_seconds("1:0:0.000"), 3600)
        self.assertEqual(convert_timestamp_str_to_seconds("0:1:0.000"), 60)
        self.assertEqual(convert_timestamp_str_to_seconds("0:0:1.000"), 1)
        self.assertEqual(convert_timestamp_str_to_seconds("2:20:23.560"), 8423)
        self.assertEqual(convert_timestamp_str_to_seconds("0:0:0"), 0)
        self.assertEqual(convert_timestamp_str_to_seconds("1:0:0"), 3600)
        self.assertEqual(convert_timestamp_str_to_seconds("1:03:0"), 3780)
        
    def test_parse_timestamp(self):
        self.assertEqual(parse_timestamp("2:20:23.560"), time(hour=2, minute=20, second=23, microsecond=560000))
        self.assertEqual(parse_timestamp("0:0:0.000"), time(hour=0, minute=0, second=0, microsecond=0))
        self.assertEqual(parse_timestamp("1:0:0"), time(hour=1, minute=0, second=0))
        self.assertEqual(parse_timestamp("0:1:45"), time(hour=0, minute=1, second=45))
    
    def test_hash_list_docs(self):
        doc1 = Document(text="Hello World", metadata={"author": "John Doe"})
        doc2 = Document(text="Hello You", metadata={"author": "Jane Austen"})
        doc3 = Document(text="Hello Me", metadata={"author": "John Doe"})
        doc4 = Document(text="", metadata={"author": "John Doe"})

        self.assertEqual(
            hash_list_docs([doc1, doc2, doc3, doc4]),
            "045e75d67a45f59a8c99522fa148e76d8aa7ad225ba74ae20f8a1755d003b4b2",
            "Hash mismatch for list of documents"
        )
        self.assertEqual(
            hash_list_docs([doc1, doc2, doc3]),
            "806db8a09fea1e20135551135be37c8bcd891435450c69fba99888272cc78b12",
            "Hash mismatch for list of documents with different length"
        )

        with self.assertRaises(TypeError):
            hash_list_docs([doc1, doc2, "doc3", doc4])
        with self.assertRaises(TypeError):
            hash_list_docs([doc1, doc2, doc3, 4])

    def test_hash_node(self):
        node1 = Node(text="Hello World", metadata={"author": "John Doe"})
        node2 = Node(text="As part of MIT course 6S099, Artificial General Intelligence",
                     metadata={'file_path': 'data/raw/sample/episode_001_large.vtt',
                               'file_name': 'episode_001_large.vtt',
                               'file_type': 'vtt',
                               'file_size': '122355',
                               'episode_number': '1',
                               'title': 'Max Tegmark: Life 3.0 | Lex Fridman Podcast #1',
                               'views': '297394',
                               'length': '4978',
                               'video_id': 'Gi8LUnhP5yU',
                               'publish_date': '2018-04-19 00:00:00',
                               'url': 'https://www.youtube.com/watch?v=Gi8LUnhP5yU',
                               'guest_names': 'Max Tegmark',
                               'episode_title': 'Life 3.0',
                               'timestamp': '00:00.000'}
                     )
        node3 = Node(text="", metadata="")
        node4 = Node(text="", metadata={"author": "John Doe"})
        node5 = Node(text="Hello World")
        node6 = Node(metadata={"author": "John Doe"})

        expected_hashes = [
            "0c94db484d909792cefeaf8f7b37f94f7e6c7a1a06b9346c4e67be99a7ff2468",
            "51e02d2a0b6760924e74050a751568c8370a78762465e9bb180cc797415ec1e0",
            "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
            "4ef8a5e5fefe8adccb68a98794a99f02f511cbf8f7249a9784ffc135d2863056",
            "a339d80c761418702b627851cbd963eb722f12dfeb360d441f9123c2d3d4fcf7",
            "4ef8a5e5fefe8adccb68a98794a99f02f511cbf8f7249a9784ffc135d2863056"]

        for i, node in enumerate([node1, node2, node3, node4, node5, node6]):
            self.assertEqual(
                hash_node(node),
                expected_hashes[i],
                f"Hash mismatch for node {i+1}"
            )

if __name__ == '__main__':
    unittest.main()
    