# -*- coding: utf-8 -*-
import base64
import os
try:
    import dill as pickle
except ImportError:
    import pickle

CALLABLE = base64.b64decode(os.environ["__PY_T_SUBMIT_CALL"])

callable = pickle.loads(CALLABLE)

callable()
