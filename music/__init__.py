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
from .data import sample_song_features

keys = ["fe_test_%04d.mp3"%i for i in xrange(1, 146)]
sol = {k:"blues" for k in keys}

@fellow.app.task(name="music.raw_features_predictions")
@typecheck.returns_dict("string", keys)
def raw_features_predictions():
    return sol


@fellow.app.task(name="music.all_features_predictions")
@typecheck.returns_dict("string", keys)
def all_features_predictions():
    return sol

@fellow.batch(name="music.all_features_model")
@typecheck.test_cases(record=sample_song_features)
@typecheck.returns("string")
def all_features_model(record):
  return "blues"

