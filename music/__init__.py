# flake8: noqa
# This file should pass flake8 in production, be sure to remove the above.
"""
This file is where fellows input their answers.
* Task names should match README
* Typecheck is used for validation, for examples browse other miniprojects
* When running `python run.py` from grader-prototype root, the default answers
herein are what is graded.
* The default answers serve to demonstrate the proper return type, and they
serve as a checkpoint for one of the correct answers in the solution. For
example, if the solution is a list of 100 elements, the default solution
should score 1%.
"""

import fellow
import typecheck


@fellow.app.task(name="music.raw_features_predictions")
@typecheck.returns("100 * string")
def food_bigrams():
    return ["blues"] * 100



@fellow.app.task(name="music.all_features_predictions")
@typecheck.returns("100 * string")
def food_bigrams():
    return ["blues"] * 100

@fellow.batch(name="music.raw_features_model")
@typecheck.test_cases(record=sample_songs)
@typeheck.returns("number")
def raw_features_model(record):
  return 0

