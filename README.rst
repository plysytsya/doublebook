==========
doublebook
==========


Imagine you have the same ebook in two different langauges and you want to
map the sentences to create a bilingual book, e.g.:

* Sentence 0 langauge a
* Sentence 0 langauge b
* Sentence 1 language a
* Sentence 1 language b


Description
===========

The SentenceMatchEngine takes two sources: text a and text b.
Both sources must represent the same text in different languages.
The goal is to match sentences of the two languages.
To achieve this it first translates text a validating the translated
sentences against sentences of text b. The core metric is a similarity-index.
If a given similarity-threshold is not reached it falls back to the translated sentence.


Note
====

This is a work in progress and does not yield reliable results yet. Feel free to contribute.