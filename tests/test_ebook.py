import os
import unittest

from doublebook.ebook import Ebook

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class EbookTest(unittest.TestCase):

    def setUp(self):
        path_to_text = os.path.join(THIS_DIR, "test_data", "zen_en.txt")
        self.ebook = Ebook(path_to_text)

    def test_read(self):
        self.ebook.read()
        self.assertIsInstance(self.ebook.content, str)

    def test_tokenize(self):
        self.ebook.tokenize()
        self.assertIsInstance(self.ebook.sentences, list)


if __name__ == '__main__':
    unittest.main(verbosity=3)
