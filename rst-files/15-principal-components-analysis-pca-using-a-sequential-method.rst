Principal components analysis (PCA) using a sequential method
=============================================================

**Author:** kevindunn

**Submitted on:** 2011-08-03 13:31:18-07:00

The singular value decomposition is usually presented as the way to calculate the PCA decomposition of a data matrix.

The NIPALS algorithm is a very computationally tractable way of calculating PCA for large data sets, since we only calculate the components we actually need; whereas SVD calculates all components in one go.

The nonlinear iterative partial least squares (NIPALS) method is more informative, as the interpretation of what the loadings and scores really mean becomes apparent when examining the above code. 

For example, in step 1 of the ``while`` loop we see the loading, :math:`p_a` contains the regression coefficients when regression the score vector, :math:`t_a`, onto each column in :math:`\mathbf{X}`. So at convergence of the while loop, any columns in :math:`\mathbf{X}` that are strongly correlated, will have similar loading values, :math:`p_a`, for those columns.


.. image:: /Data/media/images/201108/NIPALS-iterations-columns.png


*Still to come*

*  Calculating confidence limits for SPE and Hotelling's :math:`T^2` to determine which points are likely outliers

.. literalinclude:: /Data/code/2011/07/000015/principal_components_analysis_pca_using_a_sequential_method.py
	:language: python

