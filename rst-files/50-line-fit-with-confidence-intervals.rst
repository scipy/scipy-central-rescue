Line Fit with Confidence Intervals
==================================

**Author:** thomashaslwanter

**Submitted on:** 2012-11-01 01:00:34-07:00

'''
Linear regression fit

Parameters
----------
x : ndarray
    Input / Predictor    
y : ndarray
    Input / Estimator    
alpha : float
    Confidence limit [default=0.05]
newx : float or ndarray
    Values for which the fit and the prediction limits are calculated (optional)
plotFlag: int (optional)
    1 = plot, 0 = no_plot [default]
    
Returns
-------
a : float
    Intercept
b : float
    Slope
ci : ndarray
    Lower and upper confidence interval for the slope
info : dictionary, containing return information on
    - residuals
    - var_res
    - sd_res
    - alpha
    - tval
    - df
newy : list(ndarray)
    Predictions for (newx, newx-ciPrediction, newx+ciPrediction)

Examples
--------
>>> import numpy as np
>>> from fitLine import fitLine
>>> x = np.r_[0:10:11j]
>>> y = x**2
>>> (a,b,(ci_a, ci_b),_)=fitLine(x,y)    

Notes
-----
Example data and formulas are taken from
D. Altman, "Practical Statistics for Medicine"
'''

'''
author : thomas haslwanter
date : 28 oct 2012
ver : 1.1
'''

.. literalinclude:: /Data/code/2012/11/000050/line_fit_with_confidence_intervals.py
	:language: python

