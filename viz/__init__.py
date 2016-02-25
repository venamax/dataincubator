import fellow
import typecheck

@fellow.app.task(name="viz.counts_by_hour")
@typecheck.returns("string")
def counts_by_hour():
    return "http://a-b-c.herokuapp.com"

@fellow.app.task(name="viz.live_count_boxplot")
@typecheck.returns("string")
def live_count_boxplot():
    return "http://a-b-c.herokuapp.com"

@fellow.app.task(name="viz.map_static")
@typecheck.returns("string")
def map_static():
    return "http://a-b-c.herokuapp.com"

@fellow.app.task(name="viz.map_animated")
@typecheck.returns("string")
def map_animated():
    return "http://a-b-c.herokuapp.com"
