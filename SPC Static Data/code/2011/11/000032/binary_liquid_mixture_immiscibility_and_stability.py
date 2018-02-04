# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0
#Determines regions of immiscibility and any limits of essential instability 
#for a binary liquid mixture of components B and C. the excess Gibbs energy of 
#mixing is given explicitly by an empirical equation: 
#deltaGex/RT = xBxC[k1+k2(xB-xC)+k3(xB-xC)^2] where xB+xC=1

import numpy as np
from matplotlib.pylab import *

# These are the functions called by the bisection method
def f(x, id):
    if id == 1:
        return (-2 * (k1 + k2 * (6 * x - 3) + k3 * (24 * x**2 - 24 * x + 5)) 
                + 1 / (x - x**2))
    elif id == 2:
        return (-2 * k1 * x + k1 + k2 * (-6 * x**2 + 6 * x - 1) + k3 * 
                ( -16 * x**3 + 24 * x**2 - 10 * x + 1) + log(x) - log(1 - x))
    elif id == 3:
        return (dummys - (-2 * k1 * x + k1 + k2 * (-6 * x**2 + 6 * x - 1) + 
                          k3 * (-16 * x**3 + 24 * x**2 - 10 * x + 1) + 
                          log(x) - log(1 - x)))

#This function is to calculate values for the y-axis on the figure
def g(x):
    return (x * (1 - x) * (k1 + k2 * (x - (1 - x)) + k3 * (x - (1 - x))**2) + 
            x * log(x) + (1 - x) * log(1 - x))

#The incremental search method is used to start off the bisection method    
def incremental(x0,xf,id):
    dx = (xf - x0) / 998
    for i in range(998):
        y1 = f(x0,id)
        y2 = f(x0 + (i + 1) * dx,id)
        if y1 * y2 < 0:
            for j in range(10):
                y1 = f(x0 + i * dx,id)
                y2 = f(x0 + i * dx + (j + 1) * dx/10,id)
                if y1 * y2 < 0:
                    x1 = x0 + i * dx + j * dx / 10
                    x2 = x0 + i * dx + (j + 1) * dx / 10
                    y1 = f(x1,id)
                    y2 = f(x2,id)
                    return x1, x2, y1, y2
                
# Bisection method used to solve for non-linear equation
def bisec(x0,xf,id):
    x1, x2, y1, y2 = incremental(x0,xf,id)
    e = 1
    while e > 1e-6:
        x3 = (x1 + x2) / 2
        y3 = f(x3,id)
        if y1 * y3 < 0:
            x2 = x3
            y2 = y3
        else:
            x1 = x3
            y1 = y3
        e = abs(1 - (x1 / x2))
    return x2

# Constants
k1 = 2.0
k2 = 0.2
k3 = -0.8

#Set up vectors of composition values
xB = np.linspace(0.001,0.999,101)
xC = 1 - xB

#This is deltaG/RT calculated from the excess Gibbs given at top
deltaGoverRT = (xB * xC * (k1 + k2 * (xB - xC) + k3 * (xB - xC)**2) + 
                xB * log(xB) + xC * log(xC))
#First and second derivative of deltaG/RT
derivative = (-2 * k1 * xB + k1 + k2 * (-6 * xB**2 + 6 * xB - 1) + k3 * 
              (-16 * xB**3 + 24 * xB**2 - 10 * xB + 1) + log(xB) - log(1 - xB))
derivative2 = (-2 * (k1 + k2 * (6 * xB - 3) + k3 * (24 * xB**2 - 24 * xB + 5)) 
               + 1 / (xB - xB**2))

#find spinodal points for instability region using bisection method
xspin1 = bisec(0.001, 0.999, 1)
xspin2 = bisec(xspin1, 0.999, 1)

#initial guess at binodal points at minima of function
xB1 = bisec(0.001, 0.999, 2)
xB2 = bisec(xB1, 0.999, 2)
xB3 = bisec(xB2, 0.999, 2)

xBa = xB1
xBb = xB3

#Solve for binodal points using bisection method
converged = False
while not converged:
    dummys = (g(xBb) - g(xBa)) / (xBb - xBa)      #dummy slope
    e = abs(1 - (dummys / f(xBb, 2)))
    if e < 1e-4:
        converged = True
    else:
        xBa = bisec(0.001, 0.999, 3)
        xBu = bisec(xBa, 0.999, 3)
        xBb = bisec(xBu, 0.999, 3)
    
yint = g(xBa) - dummys * xBa
y = yint + dummys * xB

figure()
plot(xB, deltaGoverRT, '-')
plot(xB, y, '-')
plot(xB1, g(xB1), '.', color='blue', markersize=12)
plot(xB3, g(xB3), '.', color='blue', markersize=12)
plot(xBa, g(xBa), '.', color='red', markersize=12)
plot(xBb, g(xBb), '.', color='red', markersize=12)
plot(xspin1, g(xspin1), '.', color='orange', markersize=12)
plot(xspin2, g(xspin2), '.', color='orange', markersize=12)
grid('on')
xlabel(' xB ')
ylabel(' deltaG/RT ')
title('DeltaG/RT vs xB')
show()

print 'There is one-phase instability between xB = ', "%.2f" % xspin1, 
'and xB = ', "%.2f" % xspin2
print '(Orange points on figure, "spinodal points")'
print 'The region of immiscibility is between xB = ', "%.2f" % xBa, 
'and xB = ', "%.2f" % xBb
print '(Red points on figure, "binodal points")'
print 'Blue points on fig show minima, which do not equal to the binodal points'