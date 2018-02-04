Process Identification by means od the Step Response approach
=============================================================

**Author:** jonathan-ospino-pinedo

**Submitted on:** 2013-02-28 17:43:41-08:00

This code snippet provides to the user the possibility of approximating a dynamical system to a *First-Order-Plus-Dead-Time (FOPDT)* dynamical systems using the "Fit 3" approach commented in *"Principles and Practice of Automatic Process Control"* (Corrpio & Smith, 2005).

For the python function described in the previous code, the user has to call the function according to *steptestingtxt('FILENAME.TXT')*. For more information about the function, call the function docstring in the ipython console by means of *steptesting?* or look inside the script file *.py.

**Example**

A test data file was supplied. The basic structure of this *.TXT file has the form {t, u, y}, where *t*, *u*, and *y* correspond to the *time*, the *input signal*, and the *response signal* respectively. After calling the function with this data set, the results are displayed in a graphical way as in the following figure:



.. image:: /Data/media/images/201302/sample_pysteptestingtxt_1.png

If used in an interactive ipython console the function also will print some text on the console prompt.

.. literalinclude:: /Data/code/2013/02/000061/process_identification_by_fitting_a_first_order_plus_dead_time_response_curve.py
	:language: python
