# Python torque submitter

This is as very simple hackish hack, that allows you to run tasks as
as torque jobs.

Features:

* Allows you to sent enviorment on the other side
* Allows to execute any callable function (provided that it is defined)

Works by serializing the enviorment and callable function to the
enviorment variables (beware there is size limit --- althrough it is in
range of megabytes).

