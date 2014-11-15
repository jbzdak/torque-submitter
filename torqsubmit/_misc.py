# -*- coding: utf-8 -*-


def update_environ(store):
    import os
    os.environ['PBS_NP'] = str(store.cpus_per_task)


def callable_executor(data):
    store, ii = data
    task = store.get_task(ii)
    task()


def exec_many_func(arg):
    """
    A function that executes all functions passed in arguments.
    :param list arg: callables
    """
    for f in arg:
        f()
