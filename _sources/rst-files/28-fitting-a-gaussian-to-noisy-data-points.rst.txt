Fitting a Gaussian to noisy data-points
=======================================

**Author:** stefan

**Submitted on:** 2011-09-22 19:43:41-07:00

This script reproduces the plots from

  H. Guo, *A Simple Algorithm for Fitting a Gaussian Function*, IEEE Signal Processing Magazine, September 2011,
  pp. 134--137.

The paper describes how to fit a Gaussian function to a set of noisy data-points.  I.e., given points ``(x, y)``, find the parameters :math:`A` (amplitude), :math:`\mu` (mean) and :math:`\sigma` (standard deviation) such that

.. math::

   y \sim A e^{-(x - \mu)^2 / 2 \sigma^2}.

The paper illustrates four methods:

 1. Least squares fit of a parabola on log(y).
 2. Same as 1 but using only values of y where y > T.
 3. Weighted least squares fit, with y-values as weights.
 4. Iterative weighted least squares fit: iteration of method 3,
    but estimating y's from the fitted model after each round.

This script generates two examples: an easy one, on which methods 1 to 3 are successful, followed by a harder one on which only method 4 works.


.. image:: /Data/media/images/201109/gauss_fit.png

.. literalinclude:: /Data/code/2011/09/000028/fitting_a_gaussian_to_noisy_data_points.py
	:language: python

