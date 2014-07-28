#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import base64
import tempfile
import sys

RUN_SCRIPT = """
#!/bin/bash

{env}

python {file}
exit $?
"""

INIT_ENV = base64.b64decode(os.environ["__PY_T_SUBMIT_ENV"])

ROOT_DIR = os.environ["__PY_T_SUBMIT_DIRNAME"]
EXECUTOR = os.path.join(ROOT_DIR, 'torque_executor.py')

init_file = tempfile.NamedTemporaryFile(suffix=",sh", delete=False)

init_file.write(RUN_SCRIPT.format(env=INIT_ENV, file=EXECUTOR))
init_file.flush()

sys.exit(os.system("bash " + init_file.name))