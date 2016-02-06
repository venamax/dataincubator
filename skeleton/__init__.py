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

from .data import sample_jsons_for_validation

# Example of a list result
@fellow.app.task(name="skeleton.visit_the_boneyard")
@typecheck.returns("5 * (count, number)")
def boneyard():
  return [(13, 0.814)] * 5

# Example of a dict result
keys = ["waltz", "rumba", "blues"]
@fellow.app.task(name="skeleton.the_dance_macabre")
@typecheck.returns_dict("number", keys)
def the_dance_macabre():
  return {"waltz": 0.,
          "rumba": 0.,
          "blues": 0.,
         }

# Example of a model result
@fellow.batch(name="skeleton.ossification_commencing")
@typecheck.test_cases(record=sample_jsons_for_validation)
@typeheck.returns("number")  # Whatever the model output is
def ossification_commencing(record):
  return 0

