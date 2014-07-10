# -*- coding: utf-8 -*-
import base64
import multiprocessing
import os
import sys
from torqsubmit.store import load_store, Mode, TorqeSubmitStore
from torqsubmit._misc import callable_executor, update_environ

store = load_store()

assert isinstance(store, TorqeSubmitStore)

if store.mode == Mode.SINGLE_TASK:
    store.task()
    sys.exit(0)

cpus = os.environ.get("PBS_NP", 1)
tasks = store.tasks


if cpus == 1:
    for t in tasks():
        t()
else:
    processes = int(cpus / store.task_concurrency)
    p = multiprocessing.Pool(processes, initializer=update_environ, initargs=store, maxtasksperchild=store.max_tasks_per_child)
    p.map(callable_executor, store.tasks_serialized, chunksize=store.map_chunksize)
    p.join()
    p.close()
