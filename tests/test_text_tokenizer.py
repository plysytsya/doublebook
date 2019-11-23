import os
import unittest

from doublebook.text_tokenizer import TextTokenizer

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(THIS_DIR)
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')


class TextTokenizerTest(unittest.TestCase):

    def setUp(self):
        path_mock_text = os.path.join(THIS_DIR, "test_data", "lorem_ipsum.txt")
        with open(path_mock_text) as file:
            self.tokenizer = TextTokenizer(file.read())

    def test_1_tokenize(self):
        sentences = self.tokenizer.tokenize()
        self.assertTrue(isinstance(sentences, list))


if __name__ == '__main__':
    unittest.main(verbosity=3)
