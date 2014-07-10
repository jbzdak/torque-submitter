# -*- coding: utf-8 -*-

from __future__ import print_function
from functools import partial

callable = partial(print, "Hello World!")

from torqsubmit import submit, Submitter

s = Submitter()
s.tasks = [callable]
s.submit()

