# -*- coding: utf-8 -*-

from __future__ import print_function
from functools import partial
from torqsubmit.store import EnvStore

callable = partial(print, "Hello World!")

from torqsubmit._submit import Submitter


ENV = """
source ${HOME}/.bashrc
workon torque-submit
export MSG="Hello World!"
"""


def print_from_env(id):
    import os
    import time
    import datetime
    print (datetime.datetime.now())
    print (os.environ["MSG"])
    print (os.environ["PBS_ARRAYID"], id)
    time.sleep(60)


s = Submitter()
s.StoreClass = EnvStore
s.use_pbs_array = True
s.array_tasks_to_run_in_paralel = None
s.enviorment = ENV
s.tasks = [partial(print_from_env, ii) for ii in range(80)]
s.submit()
# -*- coding: utf-8 -*-