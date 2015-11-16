import fellow
import typecheck

@fellow.app.task(name="assignment1.add")
@typecheck.test_cases(x=[1, 2], y=[5, 6.0])
@typecheck.returns("number")
def add(x, y):
    return x + y
