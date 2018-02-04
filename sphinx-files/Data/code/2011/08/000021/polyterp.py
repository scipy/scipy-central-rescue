"""
Polynomial interpolation function/class (up to 3rd order).
"""

## Copyright 2011, Jonathan Stickel.
## All rights reserved.

## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice,
##    this list of conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright
##    notice, this list of conditions and the following disclaimer in the
##    documentation and/or other materials provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY JONATHAN STICKEL ''AS IS'' AND ANY EXPRESS OR
## IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
## MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
## EVENT SHALL JONATHAN STICKEL OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
## INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
## (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
## LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
## ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
## THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

## The views and conclusions contained in the software and documentation are
## those of the authors and should not be interpreted as representing official
## policies, either expressed or implied, of Jonathan Stickel.


import numpy as np
import scipy.linalg as lnag
from scipy import sparse
from scipy.sparse import linalg as spla


def zeroterp(x,xp):
    """
    Find the indexes for 'zero' interpolation.
    
    Parameters
    __________
    x : 1D array
        A 1-D array of monotonically increasing real values.
        Monotonicity is assumed and is NOT checked.
    xp : 1D array
        A 1-D array (or scalar) of interpolant x values.  Need not be
        monotonic.
        
    Returns
    _______
    idx : 1D array
        The indeces for for zero interpolation.

    Notes
    _____
    This function is faster than:
    scipy.interpolate.interp1d(x,np.arange(x.size),kind='zero')(xp).astype(int)
    and allows extrapolation.
    """
    if np.isscalar(xp):
        xp = np.array([xp])
    idx = np.searchsorted(x,xp,'right') - 1
    if xp.min()<x.min() or x.max()<=xp.max():
        idx[idx==-1] += 1   # could use idx.clip() instead ?
        idx[idx==x.size-1] += -1
        print('Warning: extrapolation performed (or equal maximums)')
    return idx


class interpolate(object):
    """
    interpolate(x,y=None,xp=None,n=3)
    
    Interpolate using simple, piecewise polynomial interpolation (NOT
    splines). No differential constraints are used and the interpolants are not
    necessarily continuous.
    
    Parameters
    __________
    x : 1D array
        A 1-D array of monotonically increasing real values.
        Monotonicity is assumed and is NOT checked.
    y : 1D array
        Real values corresponding to x.
    xp : 1D array
        A 1-D array (or scalar) of interpolant x values.  Need not be
        monotonic.
    n : scalar
        Order of interpolation (0-3).  Default is 3rd order (cubic) if
        not provided.

    Either y OR xp must be provided to initialize the function
    object. The other is given as input when subsequently calling the
    function.

    Notes
    _____
    The polynomial interpolation implemented here consists of fitting an
    nth-order polynomial segment centered at each point (for even n) or between
    points (for odd n).  The fitting can be put in matrix form as

    X*a = H*y

    Where X is a block diagonal matrix where each block (B) is a local
    Vandermonde matrix about a point and H is a mapping matrix.  The polynomial
    coefficients are to be solved for in 'a'.  This formulation can be used in
    two ways.  For many different values of x ('xp'), 'a' can be solved for
    explicitly, and the interpolated values yp for each xp can be calculated by

    yp = Xp*a

    where is Xp is the block Vendermonde matrix for xp.  Alternatively, for
    many different values for y, but only one set of xp, we can write

    yp = Xp*inv(X)*H*y = P*y

    where P = Xp*inv(X)*H.  Clearly this form requires an explicit inverse for
    X.  Althought inverting matrices should usually be avoided, in this case
    the inverse can be obtained in a robust manner by taking advantage of the
    fact that X is block diagonal.
    """
    
    def __init__(self,x,y=None,xp=None,n=3):
        self.x = x
        self.n = n
        self.N = x.size
        self.H = self.formH()
        self.B = self.formBs()
        
        if y is not None: # xp will be provided subsequently; solve for 'a'
            self.ygiven = True
            self.usemessage = 'Function object should be provided xp (interpolating x values) since the y values were already given'

            self.y = y
            self.X = self.formX()
            self.a = self.polycoefs(y)
            
        else: # y will be provided subsequently; build 'P'
            self.ygiven = False
            self.usemessage = 'Function object should be provided y (values corresponding to x) since xp (interpolating points) were already given'

            self.Xinv = self.formXinv()
            self.xp = xp
            self.Xp = self.formXp(xp)
            self.P = self.formP()


    #### do user interface stuff later if necessary... #####
    ## def check_input(self):
    ##     """
    ##     Check that inputs are valid
    ##     """
    ##     if y is None and xp is None:
    ##         raise ValueError('
        

    def __call__(self,v):
        """
        The function call for the object.  Find the interpolated y
        values for either new 'y' or new 'x'.
        """
        if self.ygiven:
            xp = v
            Xp = self.formXp(xp)
            return Xp*self.a
        else:
            y = v
            return self.P*y


    def formH(self):
        """
        Form the 'H' matrix s.t. X*a = H*y.
        """
        n = self.n
        N = self.N
        nn = n+1
        i = np.arange(nn*(N-n))
        j = np.array([range(k,N-nn+1+k) for k in range(nn)]).transpose().flatten()
        v = np.ones(nn*(N-n))
        H = sparse.coo_matrix( (v,(i,j)), shape=(nn*(N-n),N) )
        return H.tocsr()


    def formBs(self):
        """
        Form the 'B' matrices, i.e. the Vandermonde matrices that are the
        'blocks' in X, where X*a = H*y.
        """
        x = self.x
        N = self.N
        n = self.n
        nn = n+1
        B = [np.vander(x[j:j+nn],nn) for j in xrange(N-n)]
        return B


    def formX(self):
        """
        Form the 'X' matrix, i.e. the block-diagonal Vandermonde matrix,
        s.t. X*a = H*y.
        """
        N = self.N
        n = self.n
        B = np.array(self.B)
        X = sparse.bsr_matrix( (B,range(N-n),range(N-n+1)) )
        return X.tocsr()


    def formXinv(self):
        """
        Form the inverse of the 'X' matrix, i.e. the block-diagonal
        Vandermonde matrix, s.t. X*a = H*y.

        Note: the inverse computation is fast and stable by making using
        of the fact that X is block diagonal.
        """
        N = self.N
        n = self.n
        B = self.B
        #Binv = np.array([lnag.inv(B[j]) for j in xrange(N-n)])
        Binv = np.array([lnag.inv(b) for b in B])
        Xinv = sparse.bsr_matrix( (Binv,range(N-n),range(N-n+1)) )
        return Xinv.tocsr()


    def polycoefs(self,y):
        """
        Determine the set of polynomial coefficients 'a' s.t. yp = Xp*a.

        Parameters
        ___________________
        x : 1D array
            A 1-D array of monotonically increasing real values.
            Monotonicity is assumed and is NOT checked.
        y : 1D array
            Real values corresponding to x.
        n : scalar
            Order of interpolation (0-3).

        Returns
        ___________________
        a : 1D array
            The set of polynomial coefficients.
        """
        H = self.H
        X = self.X
        a = spla.spsolve(X,H*y)
        return a


    def formXp(self,xp):
        """
        Form the 'Xp' matrix s.t. yp = Xp*a, where 'a' is the set of
        interpolating polynomial coefficients.

        Parameters
        ___________________
        x : 1D array
            A 1-D array of monotonically increasing real values.
            Monotonicity is assumed and is NOT checked.
        xp : 1D array
            A 1-D array (or scalar) of interpolant x values.  Need not be
            monotonic.

        Returns
        ___________________
        Xp : 2D array
            The 'Xp' matrix returned as numpy array.
        """
        n = self.n
        x = self.x
        N = self.N
        nn = n+1
        Np = xp.size
        Bp = np.vander(xp,nn)
        # find indexes that map xp to x
        #idx = ipt.interp1d(x, np.arange(N), 'zero')(xp).astype(int)
        idx = zeroterp(x,xp)
        if n==0 or n==1:
            1 # do nothing
        elif n==2:
            # correct for interpolation on final segment
            idx[idx==N-2] += -1
        elif n==3:
            # correct for interpolation on end segments
            # could use "np.clip" to do this!  JJS 4/26/11
            idx[idx==0] += 1
            idx[idx==N-2] += -1
            idx = idx - 1
        else:
            raise NotImplementedError('n == %g is not implemented' % n)    
        i = np.array(range(Np)*nn)
        j = np.array([ nn*idx[range(Np)]+k for k in range(nn) ]).flatten()
        v = Bp.transpose().flatten()
        Xp = sparse.coo_matrix( (v,(i,j)), shape=(Np,nn*(N-n)) )
        return Xp.tocsr()


    def formP(self):
        """
        Form the interpolating matrix 'P' s.t. yp = P*y.

        Parameters
        ___________________
        x : 1D array
            A 1-D array of monotonically increasing real values.
            Monotonicity is assumed and is NOT checked.
        xp : 1D array
            A 1-D array (or scalar) of interpolant x values.  Need not be
            monotonic.
        n : scalar
            Order of interpolation (0-3).

        Returns
        ___________________
        P : 2D array
            The interpolating matrix (returned as numpy array).
        """
        return self.Xp*self.Xinv*self.H
