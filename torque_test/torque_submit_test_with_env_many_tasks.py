# -*- coding: utf-8 -*-

from __future__ import print_function
from functools import partial

callable = partial(print, "Hello World!")

from torqsubmit._submit import submit, Submitter


ENV = """
source ${HOME}/.bashrc
workon torque-submit
export MSG="Hello World!"
"""


def print_from_env():
    import os
    print(os.environ["MSG"])


s = Submitter()
s.enviorment = ENV
s.tasks = [print_from_env, print_from_env]
s.submit()
