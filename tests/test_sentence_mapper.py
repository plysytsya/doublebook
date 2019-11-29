import os
import unittest
import warnings

import numpy as np
import pandas as pd

from doublebook.sentence_mapper import SentenceMapper

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(THIS_DIR)


def get_mock_text(path):
    with open(path) as file:
        return file.read()


class SentenceMapperTest(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        path_en = os.path.join(THIS_DIR, "test_data", "huckfinn_en.txt")
        path_de = os.path.join(THIS_DIR, "test_data", "huckfinn_de.txt")
        self.mapper = SentenceMapper(path_en, path_de, "en", "de")
        self.source_sentence = "Hello, world!"
        self.target_sentences = [
            "The gras is green",
            "The glass is half full",
            "Hello, python!"
        ]

    def test_get_similarity_indexes(self):
        similarity_indexes = self.mapper.get_similarity_indexes(self.source_sentence, self.target_sentences)
        self.assertIsInstance(similarity_indexes, np.ndarray)

    def test_get_most_similar_sentence(self):
        most_similar = self.mapper.get_most_similar(self.source_sentence, self.target_sentences)
        self.assertEqual(most_similar.get('sentence'), self.target_sentences[2])

    def test_map_sentences(self):
        mapped_sentences = self.mapper.map_sentences()
        for index, result in enumerate(mapped_sentences):
            print("sentence number:", index)
            print(result)
            print('---------')
        df = pd.DataFrame(mapped_sentences)
        df.to_csv(os.path.join(THIS_DIR, "tmp", "test3.csv"))

    def test_get_relative_distance(self):
        test_cases = [[5, 4, 0.8], [1, 1, 1], [0, 0, 1]]
        for case in test_cases:
            relative_distance = self.mapper.get_relative_distance(case[0], case[1])
            self.assertEqual(relative_distance, case[2])

    def test_add_stats(self):
        schema = ["source", "mapped", "similarity", "wordcount_source", "wordcount_mapped"]
        source_sentence = "Simple is better than complex."
        most_similar = {"sentence": "Einfach ist besser als komplex.", "similarity_index": 0.84}
        self.mapper.target_sentences = [most_similar.get('sentence')]
        statistics = self.mapper.add_statistics(0, source_sentence, most_similar)
        self.assertIsInstance(statistics, dict)
        for key in schema:
            self.assertIn(key, statistics.keys())

    def test_reduce_target_sentence_pool(self):
        self.mapper.source_sentences = [x for x in range(100)]
        self.mapper.target_sentences = [x for x in range(100)]
        self.mapper.max_position_deviation = 0.1
        reduced = self.mapper.reduce_target_sentence_pool(20)
        self.assertEqual(reduced, [x for x in range(10, 30)])


if __name__ == '__main__':
    unittest.main(verbosity=3)
