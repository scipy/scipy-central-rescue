# Limitations: does not handle missing data

import numpy as np

# Download the CSV data file from: 
# http://datasets.connectmv.com/info/silicon-wafer-thickness
raw = np.genfromtxt('silicon-wafer-thickness.csv', delimiter=',', skip_header=1)
N, K = raw.shape

# Preprocessing: mean center and scale the data columns to unit variance
X = raw - raw.mean(axis=0)
X = X / X.std(axis=0)

# Verify the centering and scaling
X.mean(axis=0)   # array([ -3.92198351e-17,  -1.74980803e-16, ...
X.std(axis=0)    # [ 1.  1.  1.  1.  1.  1.  1.  1.  1.]

# We are going to calculate only 2 principal components
A = 2

# We could of course use SVD ...
u, d, v = np.linalg.svd(X)
 
# Transpose the "v" array from SVD, which contains the loadings, but retain 
# only the first A columns
svd_P = v.T[:, range(0, A)]  
 
# Compute the scores from the loadings:
svd_T = np.dot(X, svd_P)

# But what if we really only wanted calculate A=2 components (imagine SVD on
# a really big data set where N and K >> 1000). This is why will use the NIPALS,
# nonlinear iterative partial least squares, method.

nipals_T = np.zeros((N, A))
nipals_P = np.zeros((K, A))

tolerance = 1E-10
for a in range(A):
    
    t_a_guess = np.random.rand(N, 1)*2
    t_a = t_a_guess + 1.0
    itern = 0

    # Repeat until the score, t_a, converges, or until a maximum number of 
    # iterations has been reached
    while np.linalg.norm(t_a_guess - t_a) > tolerance or itern < 500:
         
        # 0: starting point for convergence checking on next loop
        t_a_guess = t_a

        # 1: Regress the scores, t_a, onto every column in X; compute the
        #    regression coefficient and store it in the loadings, p_a
        #    i.e. p_a = (X' * t_a)/(t_a' * t_a)
        p_a = np.dot(X.T, t_a) / np.dot(t_a.T, t_a)


        # 2: Normalize loadings p_a to unit length
        p_a = p_a / np.linalg.norm(p_a)

        # 3: Now regress each row in X onto the loading vector; store the
        #    regression coefficients in t_a.
        #    i.e. t_a = X * p_a / (p_a.T * p_a)
        t_a = np.dot(X, p_a) / np.dot(p_a.T, p_a)

        itern += 1

    #  We've converged, or reached the limit on the number of iteration
    
    # Deflate the part of the data in X that we've explained with t_a and p_a
    X = X - np.dot(t_a, p_a.T)
    
    # Store result before computing the next component
    nipals_T[:, a] = t_a.ravel()
    nipals_P[:, a] = p_a.ravel()
    

# PCA also has two very important outputs we should calculate:

# The SPE_X, squared prediction error to the X-space is the residual distance 
# from the model to each data point. 
SPE_X = np.sum(X**2, axis=1)

# And Hotelling's T2, the directed distance from the model center to
# each data point. 
inv_covariance = np.linalg.inv(np.dot(nipals_T.T, nipals_T)/N)
Hot_T2 = np.zeros((N, 1))
for n in xrange(N):
    Hot_T2[n] = np.dot(np.dot(nipals_T[n,:], inv_covariance), nipals_T[n,:].T)

# You can verify the NIPALS and SVD results are the same:
# (you may find that the signs have flipped, but this is still correct)
nipals_T / svd_T
nipals_P / svd_P

# But since PCA is such a visual tool, we should plot the SPE_X and 
# Hotelling's T2 values
from matplotlib import pylab
pylab.plot(SPE_X, 'r.-')  # see how observation 154 is inconsistent
pylab.plot(Hot_T2, 'k.-') # observations 38, 39,110, and 154 are outliers

# And we should also plot the scores:
pylab.figure()
pylab.plot(nipals_T[:,0], nipals_T[:,1], '.')
pylab.grid()

# Confirm the outliers in the raw data, giving one extra point above and below
raw[37:41,:]
raw[109:112,:]
raw[153:156,:]

# Next step for you: exclude observation 38, 39, 110 and 154 and 
# rebuild the PCA model. Can you interpret what the loadings, nipals_P, mean?
