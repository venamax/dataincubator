# -*- coding: utf-8-*-
import fellow
import typecheck

@fellow.app.task(name="sql.score_by_zipcode")
@typecheck.returns("183 * (string, number, number, count)")
def score_by_zipcode():
    return [("11201", 21.9060928719313812, 0.179441607823702, 6762)] * 183


@fellow.app.task(name="sql.score_by_map")
@typecheck.returns("string")
def score_by_map():
    # must be url starting with ctb.io
    return "http://cdb.io/"

@fellow.app.task(name="sql.score_by_borough")
@typecheck.returns("5 * (string, number, number, count)")
def score_by_borough():
    return [("MANHATTAN", 22.2375933589636849, 0.0332739265922062, 204185)] * 5

@fellow.app.task(name="sql.score_by_cuisine")
@typecheck.returns("75 * (string, number, number, count)")
def score_by_cuisine():
    return [("French", 21.9985734664764622, 0.177094690841052, 7010)] * 75

@fellow.app.task(name="sql.violation_by_cuisine")
@typecheck.returns("20 * ((string, string), number, count)")
def violation_by_cuisine():
    return [(("Café/Coffee/Tea", "Toilet facility not maintained and provided with toilet paper; waste receptacle and self-closing door."), 1.8836420929815939, 315)] * 20
