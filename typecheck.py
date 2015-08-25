from __future__ import print_function

import json
import pyparsing as pp

length = pp.Word(pp.nums).setParseAction(lambda tokens: int(tokens[0]))

def array_validator(tokens):
    length, subschema = tokens
    return {"type": "array", "minItems": length, "maxItems": length,
            "items": subschema}

def tuple_validator(tokens):
    length = len(tokens)
    return {"type": "array",
            "items": tokens.asList(),
            "minItems": length,     # prevent missing items
            "maxItems": length}     # prevent extra items

number = pp.Literal("number").setParseAction(lambda: {"type": "number"})
string = pp.Literal("string").setParseAction(lambda: {"type": "string"})
count = pp.Literal("count") \
          .setParseAction(lambda: {"type": "integer", "minimum": 0})

expr = pp.Forward()
tuple = (pp.Suppress(pp.Literal("(")) +
         pp.delimitedList(expr) +
         pp.Suppress(pp.Literal(")"))).setParseAction(tuple_validator)

array = (length + pp.Suppress("*") + expr).setParseAction(array_validator)
expr << (tuple | number | string | count | array)

expr = pp.LineStart() + expr + pp.LineEnd()     # throw error on extra stuff


def attach_schema(schema):
    def decorator(func):
        if not hasattr(func, "__annotations__"):
            func.__annotations__ = {}
        func.__annotations__["return"] = schema
        return func
    return decorator

def dshape_to_schema(dshape):
    try:
        return expr.parseString(dshape)[0]
    except pp.ParseException as e:
        print("Bad dshape {}".format(dshape))
        raise e

def returns_dict(dshape, keys):
    subschema = dshape_to_schema(dshape)
    schema = {"type": "object", "properties": {key: subschema for key in keys},
              "required": list(keys), "additionalProperties": False}
    return attach_schema(schema)

def returns(dshape):
    schema = dshape_to_schema(dshape)
    return attach_schema(schema)

def test_cases(**kwargs):
    def decorator(func):
        if not hasattr(func, "__annotations__"):
            func.__annotations__ = {}
        func.__annotations__.update(kwargs)
        return func
    return decorator

if __name__ == "__main__":
    import fellow       # noqa -- avoid circular imports

    tasks = {}
    for name, task in fellow.app.tasks.iteritems():
        if name.startswith("celery") or task.run.__annotations__ is None:
            continue
        schema = task.run.__annotations__["return"]
        if name.startswith("__"):
            tasks[name[2:]] = {"type": "array", "items": schema}
        else:
            tasks[name] = schema

    print(json.dumps(tasks, indent=2, sort_keys=True))
