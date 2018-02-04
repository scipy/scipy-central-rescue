Find the points at which two given functions intersect
======================================================

**Author:** kevindunn

**Submitted on:** 2011-07-17 13:36:49-07:00

The code considers the case of finding the intersection of a polynomial, :math:`y=x^2` and a line, :math:`y=x+1`.

Write these functions in the form :math:`\mathbf{f(x) = 0}`, in other words:

.. math::

    f_1(x, y) &= y - x^2 = 0\\
    f_2(x, y) &= y - x - 1 = 0 

Now write your Python function, as shown in the code, so that it accepts a vector of these inputs, :math:`x` and :math:`y`, and return another vector of outputs which contains :math:`\mathbf{f(x)}`.

Entry inspired by http://scipy.org/Cookbook/Intersection

Read the `documentation for fsolve <http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fsolve.html>`_.

.. literalinclude:: /Data/code/2011/07/000005/find_the_points_at_which_two_given_functions_intersect.py
	:language: python

