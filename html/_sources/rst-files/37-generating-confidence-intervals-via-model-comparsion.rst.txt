Generating confidence intervals via model comparsion.
=====================================================

**Author:** tillsten

**Submitted on:** 2012-03-24 18:24:24-07:00

Using leastsq to fit data it is possible to calculate an estimation of error using the 
diagonal of covariance matrix.
This has some drawbacks, especially if there is a strong dependency between the parameters. This snippet
presents another method of calculating a confidence interval using the fisher statistic of the chi^2 values.

For a longer description see:
<http://www.hearne.co.nz/attachments/RegressionBook.pdf>
Chapter 18.

The method is used and compared on a simple linear model.
Below the results is shown. The thick line in the probability plots are the error ranges calculated from the covariance matrix. It is clearly underestimating the possible error.

.. image:: /Data/media/images/201203/chi_sq_lin.png

.. literalinclude:: /Data/code/2012/03/000037/generating_confidence_intervals_via_model_comparsion.py
	:language: python

