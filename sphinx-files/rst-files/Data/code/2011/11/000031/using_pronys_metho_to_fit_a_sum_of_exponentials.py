# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0
import scipy.linalg as la
import numpy as np

def expfit(deg,x1,h,y):
    #Build matrix
    A=la.hankel(y[:-deg],y[-deg-1:])
    a=-A[:,:deg]    
    b= A[:,deg]
    #Solve it
    s=la.lstsq(a,b)[0]
    #Solve polynomial
    p=np.flipud(np.hstack((s,1)))
    u=np.roots(p)
    #Calc exponential factors
    a=np.log(u)/h
    #Build power matrix
    A=np.power((np.ones((len(y),1))*u[:,None].T),np.arange(len(y))[:,None]*np.ones((1,deg)))
    #solve it 
    f=la.lstsq(A,y)[0]
    #calc amplitudes 
    c=f/np.exp(a*x1)    
    #build x, approx and calc rms
    x=x1+h*np.arange(len(y))
    approx=np.exp(x[:,None]*a[:,None].T).dot(c[:,None])
    rms=np.sqrt(((approx-y)**2).sum())
    return a, c,rms

if __name__=='__main__':
    import matplotlib.pyplot
    x0 = 0
    step = 0.005 
    xend = 3
    x = np.arange(x0,xend+step,step)
    y = 2*exp(1.3*x)-0.5*exp(2*x)    
    error = (np.random.rand(len(y))-0.5)*1e-4;
    alpha,c,rms = expfit(2,x0,step,y+y*error)
    plt.plot(x,y,x,y+y*error)
    plt.show()
    