"""
testing simple polynomial interpolation function class
"""

import numpy as np
from matplotlib.pyplot import *
import polyterp

x = 2*np.pi*np.random.rand(7)
x.sort()
y = np.sin(x)

xp = 2*np.pi*np.random.rand(5)
xpm = np.linspace(0,2*np.pi,200)

# interpolate using polynomial coefficients
pterpra = polyterp.interpolate(x,y=y,n=3)
yp = pterpra(xp)
ypm = pterpra(xpm)

# interpolate using interpolation matrix
pterprP = polyterp.interpolate(x,xp=xp,n=3)
ypa = pterprP(y)

# check that both give the same result
print('%g = sum(yp-ypa)^2' % np.sum((yp-ypa)**2))

xfull = np.linspace(0,2*np.pi,200)
yfull = np.sin(xfull)

figure(1)
clf()
plot(x,y,'or',label='scattered')
plot(xp,yp,'sg',label='interpolated')
plot(xpm,ypm,'r',label='interpolants')
plot(xfull,yfull,'k',label='true')
legend(loc='best',numpoints=1)
draw()
show()
