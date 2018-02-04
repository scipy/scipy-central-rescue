# Source: scipy-central.org/item/23/1/plot-an-ellipse

# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0

import numpy as np
from pylab import plot, show, grid

def get_ellipse_coords(a=0.0, b=0.0, x=0.0, y=0.0, angle=0.0, k=2):
    """ Draws an ellipse using (360*k + 1) discrete points; based on pseudo code
    given at http://en.wikipedia.org/wiki/Ellipse
    k = 1 means 361 points (degree by degree)
    a = major axis distance,
    b = minor axis distance,
    x = offset along the x-axis
    y = offset along the y-axis
    angle = clockwise rotation [in degrees] of the ellipse;
        * angle=0  : the ellipse is aligned with the positive x-axis
        * angle=30 : rotated 30 degrees clockwise from positive x-axis
    """
    pts = np.zeros((360*k+1, 2))

    beta = -angle * np.pi/180.0
    sin_beta = np.sin(beta)
    cos_beta = np.cos(beta)
    alpha = np.radians(np.r_[0.:360.:1j*(360*k+1)])
 
    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)
    
    pts[:, 0] = x + (a * cos_alpha * cos_beta - b * sin_alpha * sin_beta)
    pts[:, 1] = y + (a * cos_alpha * sin_beta + b * sin_alpha * cos_beta)

    return pts

if __name__ == '__main__':

    # Plot a unit circle centered at (+2, +3)
    pts = get_ellipse_coords(a=1.0, b=1.0, x=2, y=3,k=1./8)
    ax = plot(pts[:,0], pts[:,1])

    # Set the aspect ratio so it looks like a circle; add a grid as well
    ax[0].get_axes().set_aspect(1)
    grid('on')


    # Ellipse, with major axis length = 4, minor axis = 1, centered at (0,0)
    pts = get_ellipse_coords(a=4.0, b=1.0)
    ax = plot(pts[:,0], pts[:,1])

    # Rotate the above ellipse by 30 degrees and use only 11 points!
    pts = get_ellipse_coords(a=4.0, b=1.0, angle=30,k=1./36)
    ax = plot(pts[:,0], pts[:,1])

    # Use all the options and 721 points:
    pts = get_ellipse_coords(a=2.0, b=0.25, x=-4, y=-2, angle=250,k=2)
    ax = plot(pts[:,0], pts[:,1])

    show()
