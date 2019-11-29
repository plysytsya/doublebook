import os

import gensim
import numpy as np
from nltk.tokenize import word_tokenize

from .translator import Translator
from .ebook import Ebook

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(THIS_DIR)


class SentenceMapper:

    """The SentenceMatchEngine takes two sources: text a and text b.
    Both sources must represent the same text in different languages.
    The goal is to match sentences of the two languages.
    To achieve this it first translates text a validating the translated
    sentences against sentences of text b. The core metric is a similarity-index.
    If a given similarity-threshold is not reached it falls back to the translated sentence.
    """
    def __init__(self, source_path, target_path, source_language, target_language):
        self.source_sentences = Ebook(source_path).sentences
        self.target_sentences = Ebook(target_path).sentences
        self.translator = Translator(source_language, target_language, engine="Google")
        self.max_position_deviation = 0.5

    def map_sentences(self):
        mapped = []
        for index, source_sentence in enumerate(self.source_sentences):
            translated = self.translator.translate(source_sentence)
            reduced_target_pool = self.reduce_target_sentence_pool(index)
            most_similar = self.get_most_similar(translated, reduced_target_pool)
            mapped.append(self.add_statistics(index, source_sentence, most_similar))
        return mapped

    def get_most_similar(self, source_sentence, target_sentences):
        similarity_indexes = self.get_similarity_indexes(source_sentence, target_sentences)
        position_of_sentence = np.argmax(similarity_indexes)
        return {
            "sentence": target_sentences[position_of_sentence],
            "similarity_index": similarity_indexes.max()
        }

    def reduce_target_sentence_pool(self, source_sentence_position):
        rel_source_position = source_sentence_position / len(self.source_sentences)
        max_abs_distance = round(len(self.target_sentences) * self.max_position_deviation, 0)
        abs_target_position = rel_source_position * len(self.target_sentences)
        left_border = int(round(abs_target_position - max_abs_distance, 0))
        right_border = int(round(abs_target_position + max_abs_distance, 0))
        if left_border < 0:
            left_border = 0
        return self.target_sentences[left_border:right_border]

    def get_similarity_indexes(self, source_sentence, target_sentences):
        gen_docs = [[w.lower() for w in word_tokenize(sentence)] for sentence in target_sentences]
        dictionary = gensim.corpora.Dictionary(gen_docs)
        corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
        tfidf = gensim.models.TfidfModel(corpus)
        sims = gensim.similarities.Similarity(
            os.path.join(THIS_DIR, 'tmp'), tfidf[corpus], num_features=len(dictionary))
        query_doc = [w.lower() for w in word_tokenize(source_sentence)]
        query_doc_bow = dictionary.doc2bow(query_doc)
        query_doc_tf_idf = tfidf[query_doc_bow]
        return sims[query_doc_tf_idf]

    def add_statistics(self, index, source_sentence, most_similar):
        wordcount_source = len(word_tokenize(source_sentence))
        wordcount_mapped = len(word_tokenize(most_similar.get('sentence')))
        return {
            'source': source_sentence,
            'mapped': most_similar.get('sentence'),
            'similarity': most_similar.get('similarity_index'),
            "wordcount_source": wordcount_source,
            "wordcount_mapped": wordcount_mapped,
            "absolute_distance": wordcount_source - wordcount_mapped,
            "relative_distance": self.get_relative_distance(wordcount_source, wordcount_mapped),
            "source_position": index,
            "target_position": self.target_sentences.index(most_similar.get('sentence'))
        }

    def get_relative_distance(self, wordcount_source, wordcount_mapped):
        if wordcount_source == wordcount_mapped:
            return 1
        try:
            return wordcount_mapped / wordcount_source
        except ZeroDivisionError:
            return 0


if __name__ == '__main__':
    mapper = SentenceMapper("hello", "hello", 'en', 'de')
