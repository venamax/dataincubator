# -*- coding: utf-8-*-
import fellow
import typecheck

@fellow.app.task(name="sql.score_by_zipcode")
@typecheck.returns("92 * (string, number, number, count)")
def score_by_zipcode():
    return [("11201", 9.81739130434783, 0.394278849322024, 345)] * 92

@fellow.app.task(name="sql.score_by_map")
@typecheck.returns("string")
def score_by_map():
    # must be url of the form https://x.cartodb.com/...
    return "https://cartodb.com"

@fellow.app.task(name="sql.score_by_borough")
@typecheck.returns("5 * (string, number, number, count)")
def score_by_borough():
    return [("MANHATTAN", 10.7269875502402, 0.0798259390597376, 10201)] * 5

@fellow.app.task(name="sql.score_by_cuisine")
@typecheck.returns("75 * (string, number, number, count)")
def score_by_cuisine():
    return [("French", 20.3550686378036, 0.17682605388627, 7576)] * 75

@fellow.app.task(name="sql.violation_by_cuisine")
@typecheck.returns("20 * ((string, string), number, count)")
def violation_by_cuisine():
    return [(("Café/Coffee/Tea",
              "Toilet facility not maintained and provided with toilet paper; "
              "waste receptacle and self-closing door."),
             1.87684775827172, 315)] * 20
