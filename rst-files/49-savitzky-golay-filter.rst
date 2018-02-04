Savitzky-Golay Filter
=====================

**Author:** thomashaslwanter

**Submitted on:** 2012-11-01 00:57:23-07:00

r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
The Savitzky-Golay filter removes high frequency noise from data.
It has the advantage of preserving the original shape and
features of the signal better than other types of filtering
approaches, such as moving averages techhniques.

Parameters
----------
y : array_like, shape (N,)
    the values of the time history of the signal.
window_size : int
    the length of the window. Must be an odd integer number.
order : int
    the order of the polynomial used in the filtering.
    Must be less then `window_size` - 1.
deriv: int
    the order of the derivative to compute (default = 0 means only smoothing)
rate: sampling rate (in Hz; only used for derivatives)

Returns
-------
ys : ndarray, shape (N)
    the smoothed signal (or it's n-th derivative).

Notes
-----
The Savitzky-Golay is a type of low-pass filter, particularly
suited for smoothing noisy data. The main idea behind this
approach is to make for each point a least-square fit with a
polynomial of high order over a odd-sized window centered at
the point.

The data at the beginning / end of the sample are deterimined from
the best polynomial fit to the first / last datapoints. This makes the code
a bit more complicated, but avoids wild artefacts at the beginning and the
end.

"Cutoff-frequencies":
	for smoothing (deriv=0), the frequency where
	the amplitude is reduced by 10% is approximately given by
		f_cutoff = sampling_rate / (1.5 * look)

	for the first derivative (deriv=1), the frequency where
	the amplitude is reduced by 10% is approximately given by
		f_cutoff = sampling_rate / (4 * look)

Examples
--------
Examples
--------
>>> t = np.linspace(-4, 4, 500)
>>> y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
>>> ysg = savitzky_golay(y, window_size=31, order=4)
>>> import matplotlib.pyplot as plt
>>> plt.plot(t, y, label='Noisy signal')
>>> plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
>>> plt.plot(t, ysg, 'r', label='Filtered signal')
>>> plt.legend()
>>> plt.show()

References
----------
.. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
   Data by Simplified Least Squares Procedures. Analytical
   Chemistry, 1964, 36 (8), pp 1627-1639.
.. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
   W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
   Cambridge University Press ISBN-13: 9780521880688
.. [3] Siegmund Brandt, Datenanalyse, pp 435
"""

"""
Author: Thomas Haslwanter
Version: 1.0
Date: 25-July-2012
"""



.. literalinclude:: /Data/code/2012/11/000049/savitzky_golay_filter.py
	:language: python
