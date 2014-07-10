# -*- coding: utf-8 -*-

import copy
import os
from torqsubmit.store import FileBasedStore, StoreProperty, Mode

try:
    import dill as pickle
except ImportError:
    import pickle
import base64
import subprocess

ROOT_DIR = os.path.dirname(__file__)
EXECUTOR = os.path.join(ROOT_DIR, 'torque_wrapper.py')


def submit(callable, enviorment="true", qsub_args=tuple()):
    """

    :param callable callable: Function that will be called inside torque job.
        Should be pickleable (either instancemethod of class defined on
        module level, or function defined on module level).
    :param str enviorment: Bash lines that will be executed before starting
        script that will reconstruct and call callable
    :param list qsub_args: List of arguments to qsub command
    """
    call = base64.b64encode(pickle.dumps(callable))
    enviorment = base64.b64encode(enviorment)
    environ = copy.copy(os.environ)
    environ['__PY_T_SUBMIT_ENV'] = enviorment
    environ['__PY_T_SUBMIT_CALL'] = call
    environ['__PY_T_SUBMIT_DIRNAME'] = ROOT_DIR

    call = ['qsub']
    call.append('-V')
    call.extend(qsub_args)
    call.append(EXECUTOR)

    subprocess.check_call(call, env=environ)


class Submitter(object):
    def __init__(self):
        super(Submitter, self).__init__()
        self.StoreClass = FileBasedStore
        self.tasks = {}
        self.store = {}
        self.enviorment = "true"
        self.dirname = ROOT_DIR
        self.qsub_args = tuple()
        self.processes = None
        self.memory_gb = None
        self.queue = "i3d"

    def __update_qsub_ags(self):
        result = []
        if self.processes is not None:
            result.extend(["-l", "nodes=1:ppn={}".format(self.processes)])
        if self.memory_gb is not None:
            result.extend(["-l", "mem={}GB".format(self.memory_gb)])
        if self.queue is not None:
            result.extend(["-q", self.queue])
        return result

    def __update_tasks(self):
        if len(self.tasks) == 1:
            self.store[StoreProperty.MODE] = Mode.SINGLE_TASK
            self.store[StoreProperty.TASK] = self.StoreClass.pickle_task(self.tasks[0])
        else:
            self.store[StoreProperty.MODE] = Mode.MANY_TASKS
            self.store[StoreProperty.TASK_COUNT] = len(self.tasks)
            for ii, task in enumerate(self.tasks):
                self.store[StoreProperty.TASK_NO(ii)] = self.StoreClass.pickle_task(task)


    def __update_environ(self):
        return {
            "__PY_T_SUBMIT_ENV": base64.b64encode(self.enviorment),
            "__PY_T_SUBMIT_DIRNAME": self.dirname
        }

    def submit(self):
        self.__update_tasks()
        env = dict(os.environ)
        env.update(self.__update_environ())
        env.update(self.StoreClass.save_store(self.store))
        call = ['qsub']
        call.append('-V')
        call.extend(self.qsub_args)
        call.extend(self.__update_qsub_ags())
        call.append(EXECUTOR)

        subprocess.check_call(call, env=env)
