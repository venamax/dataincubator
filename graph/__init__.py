import fellow
import typecheck

@fellow.app.task(name="graph.degree")
@typecheck.returns("100 * (string, count)")
def degree():
    return [('Alec Baldwin', 69)] * 100

@fellow.app.task(name="graph.pagerank")
@typecheck.returns("100 * (string, number)")
def pagerank():
    return [('Martha Stewart', 0.0002051725372886844)] * 100

@fellow.app.task(name="graph.best_friends")
@typecheck.returns("100 * ((string, string), count)")
def best_friends():
    return [(('David Lauren', 'Lauren Bush'), 19)] * 100
