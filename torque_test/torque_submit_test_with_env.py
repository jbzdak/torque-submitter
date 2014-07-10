# -*- coding: utf-8 -*-

from __future__ import print_function
from functools import partial

callable = partial(print, "Hello World!")

from torqsubmit._submit import submit

ENV = """
export MSG="Hello World!"
"""


def print_from_env():
    import os
    print(os.environ["MSG"])


submit(callable, enviorment=ENV)