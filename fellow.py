import subprocess
import os
from celery import Celery

n = subprocess.Popen(["netstat -nr | grep '^0\.0\.0\.0' | awk '{print $2}'"],
                     stdout=subprocess.PIPE, shell=True)
host, ___ = n.communicate()
host = host.strip()
if 'GRADER_TEST' in os.environ:
    host = 'localhost'

app = Celery("fellow", broker="amqp://" + host, backend="amqp")
app.conf.CELERY_ACCEPT_CONTENT = ["json", "pickle", "msgpack"]
app.conf.CELERY_RESULT_SERIALIZER = "json"


def batch(name):
    def decorator(func):
        app.task(func, name="__" + name)   # register func with typechecker
        @app.task(name=name)
        def inner_func(args):
            return list(map(func, args))

        inner_func.run.__annotations__ = None  # tell typechecker to ignore
        return inner_func
    return decorator

import assignment1  # noqa
import graph        # noqa
import ml           # noqa
import mr           # noqa
import nlp          # noqa
import spark        # noqa
import SQL          # noqa
import ts           # noqa
import music        # noqa

@app.task(name="celery.list_tasks")
def list_tasks():
    return app.tasks.keys()
