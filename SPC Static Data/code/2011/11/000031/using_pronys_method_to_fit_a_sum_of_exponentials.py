# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0
import scipy.linalg as la
import numpy.linalg as nla
import numpy as np

def expfit(deg,x1,h,y):
    #Build matrix
    A=la.hankel(y[:-deg],y[-deg-1:])
    a=-A[:,:deg]
    b= A[:,deg]

    #Solve it
    s=nla.lstsq(a,b)[0]
    #Solve polynomial
    p=np.flipud(np.hstack((s,1)))
    u=np.roots(p)
    #Calc exponential factors
    a=np.log(u)/h
    #Build power matrix
    A=np.power((np.ones((len(y),1))*u[:,None].T),np.arange(len(y))[:,None]*np.ones((1,deg)))
    #solve it 
    f=nla.lstsq(A,y)[0]
    #calc amplitudes 
    c=f/np.exp(a*x1)
    #build x, approx and calc rms
    x=x1+h*np.arange(len(y))

    approx=0*x
    for ii in range(len(a)):
        approx += np.exp(x*a[ii]).dot(c[ii])
    rms=np.sqrt(((approx-y)**2).sum()/len(y))

    return a, c,rms

if __name__=='__main__':
    import matplotlib.pyplot as plt
    x0 = 0
    step = 0.005
    xend = 3
    deg = 2

    a = [2, -0.5, 0.8]
#    b = [1.3+0.5*1j, 2.0, 1]
    b = [1.3, 2.0, 1]

    x = np.arange(x0,xend+step,step)
    y = 0.0
    for ii in range(len(a)):
        y += a[ii]*np.exp(b[ii]*x)
    error = (np.random.rand(len(y))-0.5)*1e-4

    beta,alpha,rms = expfit(deg,x0,step,y+y*error)

    prony = 0*x
    for ii in range(len(alpha)):
        prony += np.exp(x*beta[ii]).dot(alpha[ii])
    plt.plot(x,y, linewidth=2.0,label='Function')
    plt.plot(x,prony,'r--', linewidth=2.0,label='Prony')

    plt.legend()
    plt.show()

    print 'alfa = ' + str(alpha)
    print 'beta = ' + str(beta)
    print 'RMS = ' + str(rms)
   