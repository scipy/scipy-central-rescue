# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0 
# \file    scipy_lsFit.py
# \brief  error estimates for fit parameters using
#            bootstrap resampling
#          
# scipy.optimize.leastsq does not yield error 
# estimates for fit-parameters. As a remedy,
# one might use bootstrap resampling to get an
# impression of the respective errors
#
# \author vilo
# \date    19.03.2012
from __future__ import division
import sys
import scipy
import scipy.stats
import scipy.optimize

def myFit(data,nBins=50):
        """Fit parametric function to data.

        computes best fit of a fit-function to a the pdf of
        the input data using the method of least-squares.
        For the definition of the objective function the 
        vertical differences between the observed data
        and the fit-function is used.

        Input:
        data    -- list of values for resampling procedure
        nBin    -- number of bins for the frequency histogram

        Returns: (s)
        s       -- resulting fit-parameters
        """
        # data binning to yield frequency histogram
        freqObs,xMin,dx,nOut = scipy.stats.histogram(data,nBins)

        # prepare observed x,y-values, i.e. bin centers and
        # probability densities, respectively
        N = len(data)
        xVals = [xMin + (i+0.5)*dx    for i in range(nBins)]
        yVals = [freqObs[i]*1./(N*dx) for i in range(nBins)]
        
        # define objective function as the vertical difference
        # between the observed data and the fit-function
        fitFunc = lambda s,x: s[0]*scipy.stats.norm.pdf(x-s[1],scale=s[2])
        objFunc = lambda s,x,y: (fitFunc(s,x)-y)

        # set initial guess for the fit-parameters and perform
        # least squares fit
        s0=[1.,0.,1.]
        s,flag = scipy.optimize.leastsq(objFunc,s0,args=(xVals,yVals))

        return s

def bootstrap(data,objFunc,nBootSamp=128):
        """Empirical bootstrap resampling of data.

        estimates value of function 'objFunc' from original data 
        stored in list 'data'. Calculates corresponding error as 
        standard deviation of the 'nBootSamp' resampled bootstrap 
        data sets.

        Input:
        data        -- list of values for resampling procedure
        objFunc     -- estimator function for resampling procedure
        nBootSamp   -- number of bootstrap samples (default 128)

        Returns: (av,sDev)
        origEstim   -- value of estimFunc for original data
        resError    -- corresponding error estimated via resampling
        """
        N=len(data)
        objFuncVals = scipy.zeros(nBootSamp)
        for n in range(nBootSamp):
                resDat = data[scipy.random.randint(0,N,(N,))]
                objFuncVals[n]=objFunc(resDat)
        av   = objFunc(data) 
        # scipy.std is computed from the uncorrected variance of the 
        # data. Apply correction factor to account for bias.
        sDev = scipy.sqrt(nBootSamp/(nBootSamp-1))*scipy.std(objFuncVals)
        return av,sDev


def main():

        N     = 10000   # number of random variates
        nBoot = 500    # number of bootstrap samples 

        rawData = scipy.random.standard_normal(N)

        objFunc = lambda x: myFit(x)[2]
        av,sDev_boot = bootstrap(rawData,objFunc,nBoot)
        print 'sigma = %lf +/- %lf'%(av,sDev_boot)

main()
# EOF: scipy_lsFit.py