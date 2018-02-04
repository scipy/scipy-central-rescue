pcolor-like plotting wrapper for imshow
=======================================

**Author:** pv

**Submitted on:** 2012-11-22 09:12:09-08:00

Matplotlib's `pcolor` function becomes slow when the amount of data is large.
The work-around is to use `imshow`, but this function has a different interface
which is somewhat clumsier to use.

Here is a minimal pcolor-like wrapper function for imshow.


.. literalinclude:: /Data/code/2012/11/000055/pcolor_like_plotting_wrapper_for_imshow.py
	:language: python

