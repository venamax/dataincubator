from __future__ import absolute_import

import toolz

import typecheck
import fellow
from .data import test_json

test_json = [toolz.keyfilter(lambda k: k == "text", d)
             for d in test_json]

@fellow.batch(name="nlp.bag_of_words_model")
@typecheck.test_cases(record=test_json)
@typecheck.returns("number")
def bag_of_words_model(record):
    return 0


@fellow.batch(name="nlp.normalized_model")
@typecheck.test_cases(record=test_json)
@typecheck.returns("number")
def normalized_model(record):
    return 0


@fellow.batch(name="nlp.bigram_model")
@typecheck.test_cases(record=test_json)
@typecheck.returns("number")
def bigram_model(record):
    return 0


@fellow.app.task(name="nlp.food_bigrams")
@typecheck.returns("100 * string")
def food_bigrams():
    return ["kare kare"] * 100
