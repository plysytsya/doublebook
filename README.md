![GitHub Actions status | sdras/awesome-actions](https://github.com/plysytsya/doublebook/workflows/runtests/badge.svg)
[![codecov](https://codecov.io/gh/plysytsya/doublebook/branch/master/graph/badge.svg)](https://codecov.io/gh/plysytsya/doublebook/branch/master/graph/badge.svg)

# doublebook

The intention of this project is to create ebooks which you can use to learn a foreign language.
Imagine you have the same ebook in two different langauges and you want to
map the sentences to create a bilingual book, e.g.:

    YOU don't know about me without you have read a book by the name of The
    Adventures of Tom Sawyer; but that ain't no matter.

    Da ihr gewiß schon die Abenteuer von Tom Sawyer gelesen habt,
    so brauche ich mich euch nicht vorzustellen.

    That book was made
    by Mr. Mark Twain, and he told the truth, mainly.

    Jenes Buch hat ein gewisser Mark Twain geschrieben und was drinsteht ist wahr –
    wenigstens meistenteils.

# Description


The SentenceMatchEngine takes two sources: text a and text b.
Both sources must represent the same text in different languages.
The goal is to match sentences of the two languages.
To achieve this it first translates text a validating the translated
sentences against sentences of text b. The core metric is a similarity-index.
If a given similarity-threshold is not reached it falls back to the translated sentence.


# Note


This is a work in progress and does not yield reliable results yet. Feel free to contribute.
