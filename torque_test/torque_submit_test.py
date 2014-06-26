# -*- coding: utf-8 -*-

from __future__ import print_function
from functools import partial

callable = partial(print, "Hello World!")

from torqsubmit.submit import submit

submit(callable)

