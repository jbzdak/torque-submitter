# -*- coding: utf-8 -*-

def update_environ(task_concurrency):
    import os
    os.environ['PBS_NP'] = task_concurrency

def callable_executor(data):
    store, ii = data
    task = store.get_task(ii)
    task()