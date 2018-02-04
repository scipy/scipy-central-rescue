single input pole placement
===========================

**Author:** cknoll

**Submitted on:** 2012-04-22 05:44:43-07:00

This code calculates the gain vector of a linear feedback controller which places the eigenvalues (or "poles") of the closed loop system at desired locations in the complex plane (preferably in the open right half-plane).

For single input systems it (theoretically) yields the same result as the "place" function from a famous control system toolbox but might be less stable numerically.

Other python code for pole placement (and many other control-related things) is available on
http://sourceforge.net/projects/python-control/ (which, however, depends on some fortran code and thus might be slightly harder to install that the snippet above).

.. literalinclude:: /Data/code/2012/04/000041/single_input_pole_placement.py
	:language: python

