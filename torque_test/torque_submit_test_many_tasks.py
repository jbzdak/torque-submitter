# -*- coding: utf-8 -*-

from __future__ import print_function
from functools import partial

callable1 = partial(print, "Hello World 1!")
callable2 = partial(print, "Hello World 2!")


from torqsubmit import submit, Submitter

s = Submitter()
s.tasks = [callable1, callable2]
s.submit()
