# -*- coding: utf-8 -*-

import copy
import os
import pickle
import base64
import subprocess

ROOT_DIR = os.path.dirname(__file__)
EXECUTOR = os.path.join(ROOT_DIR, 'torque_wrapper.py')


def submit(callable, enviorment="true", qsub_args = tuple()):
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
    # call.append("-x __PY_T_SUBMIT_ENV")
    # call.append("-x __PY_T_SUBMIT_CALL")
    call.extend(qsub_args)
    call.append(EXECUTOR)

    subprocess.check_call(call, env=environ)