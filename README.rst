Python torque submitter
-----------------------

This is as very simple hackish hack, that allows you to any serializable
python callable as a torque job.

Features:

* Allows you to send enviorment on the other side
* Allows to execute any callable function as a torque task
* Allows you to launch a bunch of taska as a torque array job.

Dependencies:

* Working python 2.7 enviorment
* Some python dependencies (see ``REQUIREMENTS``)
* Working ``qsub`` command (no need for other PBS/torque stuff).

Works by serializing the enviorment and callable function to the
enviorment variables (or enviorment variables and files).
For serialization we use ``dill`` if avilable or ``pickle``.

Enviorment can be initialized using arbirtary bash script --- this script 
will be sourced before running provided python callable.

Example
=======

Example without enviorment: 

.. code-block:: python

     callable = partial(print, "Hello World!")

    from torqsubmit import Submitter

    s = Submitter()
    s.tasks = [callable]
    s.submit()


Example with enviorment:
   
.. code-block:: python

    
    callable = partial(print, "Hello World!")

    from torqsubmit._submit import Submitter

    ENV = """
    source ${HOME}/.bashrc
    workon torque-submit
    export MSG="Hello World!"
    """

    def print_from_env():
        import os
        print(os.environ["MSG"])

    s = Submitter()
    s.tasks = [callable]
    s.enviorment = ENV
    s.submit()


Example submitting many tasks:

.. code-block:: python

    from __future__ import print_function
    from functools import partial

    callable = partial(print, "Hello World!")

    from torqsubmit._submit import Submitter


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


