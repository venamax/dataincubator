from __future__ import print_function
import json
import sys

import jsonschema
import toolz

import fellow

def get_test_cases(task):
    kwarglist = toolz.keyfilter(lambda x: x != "return",
                                task.run.__annotations__)
    if kwarglist:
        value = next(kwarglist.itervalues())
        return [toolz.valmap(lambda x: x[i], kwarglist)
                for i in xrange(len(value))]
    else:
        return [{}]


def indent(string, indent="    "):
    return "\n".join(indent + line
                     for line in string.split('\n') if line)


def passes_typecheck(task):
    types = {"array": (tuple, list)}
    schema = task.run.__annotations__["return"]
    validator = jsonschema.Draft4Validator(schema, types=types)

    for test_case in get_test_cases(task):
        output = task.apply(kwargs=test_case).result
        try:
            validator.validate(output)
        except jsonschema.ValidationError as e:
            print(task.name, "failed to validate")
            print(indent(str(e)))
            return False

        try:
            json.dumps(output)
        except TypeError:
            msg = "returned a {}, which could not be serialized"
            print(task.name, msg.format(type(output)))
            return False

    return True

if __name__ == "__main__":
    failed = False
    for name, task in fellow.app.tasks.items():
        if name.startswith("celery.") or task.run.__annotations__ is None:
            continue

        if not passes_typecheck(task):
            failed = True
        else:
            print(".", end="")

    if failed:
        print("Validation Failed")
        sys.exit(1)
    else:
        print("Passed Validation")
