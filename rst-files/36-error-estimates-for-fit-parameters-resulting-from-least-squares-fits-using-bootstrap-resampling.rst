Error estimates for fit parameters resulting from least-squares fits using bootstrap resampling
===============================================================================================

**Author:** vilo

**Submitted on:** 2012-03-21 02:46:49-07:00

The function ``scipy.optimize.leastsq`` does not yield error estimates for fitted parameters.
As a remedy one might use bootstrap resampling of the underlying data in order to obtain 
error estimates for the parameters employed in the fit.

The above code snippet illustrates this for synthetic data. In the main function, a number
of N random variates from a standard normal distribution are generated, comprising the 
raw data to be processed further. The function ``myFit`` first computes an approximate 
probability density function that approximates the raw data and determines a best fit 
to a Gaussian fit function using scipy's least-squares routine. 
In the main function, the objective function is defined to return the standard deviation of 
the above fit function.
An error estimate for the parameter singled out by the objective function is obtained using
bootstrap resampling. An extensive resamling using a number of 5000 bootstrap data 
sets yields the figure below.  It illustrates the distribution of the resampled estimates of 
the standerd deviation and shows the corresponding error estimate obtained using bootstrap
resampling. The numerical value of the standard deviation reads 0.996 +/- 0.011, which is 
in good agreement with the parameters used to generate the raw data.
 

.. image:: /Data/media/images/201203/pdf_sigma_leastsq.png

.. literalinclude:: /Data/code/2012/03/000036/error_estimates_for_fit_parameters_resulting_from_least_squares_fits_using_bootstrap_resampling.py
	:language: python

