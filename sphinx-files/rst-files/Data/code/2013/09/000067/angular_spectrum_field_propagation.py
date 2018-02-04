# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0

from numpy import fft
import numpy as np
def angular_spectrum_propagation(x, y, field0, wavelength, z) :
    dx, dy = np.mgrid[-0.5:0.5:x.shape[0]*1j, -0.5:0.5:x.shape[1]*1j]
    dx *= wavelength/(x[1,0]-x[0,0])
    dy *= wavelength/(x[1,0]-x[0,0])
    dr = (dx**2 + dy**2)**.5
    dr[dr>1.] = 1.
    angular_spectrum0 = fft.fftshift(fft.fft2(field0))
    angular_spectrum1 = angular_spectrum0*np.exp(1j*2.*np.pi/wavelength*z*np.sqrt(1-dr**2))
    field1 = fft.ifft2(fft.fftshift(angular_spectrum1))
    return field1/field1.sum()*field0.sum()