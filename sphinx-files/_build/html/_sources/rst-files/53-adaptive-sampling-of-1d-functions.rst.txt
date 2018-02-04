Adaptive sampling of 1D functions
=================================

**Author:** pv

**Submitted on:** 2012-11-22 08:20:03-08:00

Sample a 1D function to given tolerance by adaptive subdivision.

The result of sampling is a set of points that, if plotted, produces a smooth curve with also sharp features of the function resolved.

This routine is useful in computing functions that are expensive to compute, and have sharp features --- it makes more sense to adaptively dedicate more sampling points for the sharp features than the smooth parts.

Examples
--------

    >>> def func(x):
    ...     '''Function with a sharp peak on a smooth background'''
    ...     a = 0.001
    ...     return x + a**2/(a**2 + x**2)
    ...
    >>> x, y = sample_function(func, [-1, 1], tol=1e-3)

    >>> import matplotlib.pyplot as plt
    >>> xx = np.linspace(-1, 1, 12000)
    >>> plt.plot(xx, func(xx), '-', x, y[0], '.')
    >>> plt.show()


.. image:: /Data/media/images/201211/sampling.png

.. literalinclude:: /Data/code/2012/11/000053/adaptive_sampling_of_1d_functions.py
	:language: python

