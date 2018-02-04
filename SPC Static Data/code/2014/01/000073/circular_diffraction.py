# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0
from numpy import *
from scipy.special import j1
from matplotlib.pyplot import *

wave = 500e-9
k = 2*pi/wave
side = 1e-6
points = 200
dim = linspace(-side/2,side/2,points)
ax,ay = meshgrid(dim,dim)
r = sqrt(ax**2 + ay**2)
area = (j1(k*r)/(k*r))**2
imshow(area)
hot()
show()
    

