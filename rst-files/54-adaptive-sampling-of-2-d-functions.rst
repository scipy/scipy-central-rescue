Adaptive sampling of 2-D functions
==================================

**Author:** pv

**Submitted on:** 2012-11-22 09:01:05-08:00

Sample a 2-D function via adaptive subdivision.

The sample points are chosen by estimating the point where the
linear and cubic interpolants based on the existing points have
maximal disagreement. This point is then taken as the next point
to be sampled.

In practice, this sampling protocol results to sparser sampling of
smooth regions, and denser sampling of regions where the function
changes rapidly, which is useful if the function is expensive to
compute.

This sampling procedure is not extremely fast, so to benefit from
it, your function needs to be slow enough to compute.

The figure below shows results from sampling the function
:math:`e^{-(x^2+y^2 - 3/4)^2/a^4)` with 2000 points.
The result from adaptive sampling is here much more accurate
than the result found by computing the function on an uniform
grid with the same number of points. (Although, for this simple
function, adaptive sampling is slower.)


.. image:: /Data/media/images/201211/sampling-2d.png

.. literalinclude:: /Data/code/2012/11/000054/adaptive_sampling_of_2_d_functions.py
	:language: python

