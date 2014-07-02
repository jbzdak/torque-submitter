Python torque submitter
-----------------------

This is as very simple hackish hack, that allows you to run tasks as
as torque jobs.

Features:

* Allows you to send enviorment on the other side
* Allows to execute any callable function (provided that it is defined)

Works by serializing the enviorment and callable function to the
enviorment variables (beware there is size limit --- althrough it is in
range of megabytes).

Enviorment can be initialized using arbirtary bash script --- this script 
will be sourced before running provided python callable. 

Example
=======

Example without enviorment: 

.. code-block:: python 
        
    from __future__ import print_function
    from functools import partial
    
    callable = partial(print, "Hello World!")
    
    from torqsubmit.submit import submit
    
    submit(callable)


Example with enviorment:
   
.. code-block:: python

    
    from __future__ import print_function
    from functools import partial
    
    callable = partial(print, "Hello World!")
    
    from torqsubmit.submit import submit
    
    ENV = """
    export MSG="Hello World!"
    """    
    
    def print_from_env():
        import os
        print(os.environ["MSG"])    
    
    submit(callable, enviorment=ENV)
 
    
