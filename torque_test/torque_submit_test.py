# -*- coding: utf-8 -*-

from __future__ import print_function
from functools import partial

callable = partial(print, "Hello World!")

from torqsubmit import Submitter

s = Submitter()
s.tasks = [callable]
s.submit()
