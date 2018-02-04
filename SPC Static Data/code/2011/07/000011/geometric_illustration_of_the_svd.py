"""Illustrate the SVD geometrically.

:author: Stefan van der Walt
:date: 2006

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import CirclePolygon
import copy

class CirclePoint(object):
    """
    Draggable arrow on a circle.

    Clicks within epsilon pixels of arrow head grab the arrow.
    """

    def __init__(self,epsilon=10):
        """Initialize circle in given axss."""
        axes = plt.gca()
        circ = CirclePolygon((0,0), 1., resolution=200)
        circ.set_fill(False)
        circ.set_edgecolor('b')
        axes.add_patch(circ)

        canvas = circ.figure.canvas
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)

        self.epsilon = epsilon
        self.circ = circ
        self.arrow = None # Created by set_angle
        self.canvas = circ.figure.canvas
        self.external_hook = None
        self.axes = axes
        self.nr_pts = 0

        self.arrow_colour = {'default': 'r', 'selected': 'g'}
        self.arrow_mode = 'default'

        self.set_angle(np.pi / 4.)

    def get_angle(self):
        """Return the angle of the arrow."""
        return self.__angle

    def set_angle(self, theta):
        """Point the arrow in the given direction."""
        self.__angle = theta

        self.update_arrow()

    angle = property(fget=get_angle, fset=set_angle,
                     doc="Angle of the arrow.")

    def update_arrow(self):
        """Redraw the canvas."""

        # Create a new arrow, and remove the previous one
        if self.arrow:
            self.axes.artists.remove(self.arrow)
        ex,ey = self.pos
        self.arrow = plt.arrow(0, 0, ex, ey, width=0.01,
                             length_includes_head=True)

        ac = self.arrow_colour[self.arrow_mode]
        self.arrow.set_edgecolor(ac)
        self.arrow.set_facecolor(ac)
        self.canvas.draw()

        if self.external_hook:
            self.external_hook()

    @property
    def pos(self):
        """Return position of arrow tip (x,y)."""
        a = self.angle
        return (np.cos(a), np.sin(a))

    def button_press_callback(self, event):
        """Called when a mouse button is pressed."""
        if event.inaxes == None: return
        if event.button != 1: return

        # translate graph coordinates to pixel coordinate
        transf = self.circ.get_transform()

        x, y = transf.transform(self.pos)
        ex, ey = event.x, event.y
        if np.sqrt((ex - x)**2 + (ey - y)**2) > self.epsilon:
            return

        # Arrow selected
        self.arrow_mode = 'selected'

        verts = self.circ.get_verts()
        verts_tf = transf.transform(verts)
        cxt = verts_tf[:, 0]
        cyt = verts_tf[:, 1]
        d = np.sqrt((cxt - ex)**2 + (cyt - ey)**2)

        self.update_arrow()

    def button_release_callback(self, event):
        """Called when a mouse button is released."""
        self.arrow_mode = 'default'
        self.update_arrow()

    def motion_notify_callback(self, event):
        """Called on mouse movement."""
        if self.arrow_mode == 'selected':
            transf = self.circ.get_transform()
            xt,yt = transf.inverted().transform((event.x, event.y))
            self.angle = -np.arctan2(xt, yt) + np.pi/2
            self.update_arrow()


class SVD_Geometry:
    def __init__(self,M):
        fig = plt.figure()

        cp = CirclePoint()
        cp.external_hook = self.plot_tf
        ax = cp.axes

        axis_max = np.array([1.5, 1.5])
        axis_min = np.array([-1.5, 1.5])

        U,S,Vt = np.linalg.svd(M)
        V = Vt.transpose()

        eig_vecs = np.vstack([(U*S).transpose(),V.transpose()])
        colours = ['m','m','c','c']
        labels = ['U', '', 'V', '']
        for i,ev in enumerate(eig_vecs):
            a = plt.arrow(0, 0, *ev, **{'width': 0.01,
                                      'length_includes_head': True})
            a.set_edgecolor(colours[i])
            a.set_facecolor(colours[i])
            plt.text(*(tuple(ev / 1.5) + tuple([labels[i]])))

            idx = (ev > axis_max)
            axis_max[idx] = ev[idx]
            idx = (ev < axis_min)
            axis_min[idx] = ev[idx]

        self.M = M
        self.cp = cp
        self.add_patch = plt.gca().add_patch

        # Maximum axis dimension is extent of bounding box
        am = max(axis_max.max(), abs(axis_min.min()))
        plt.axis('equal')
        plt.axis([-1.5*am, 1.5*am, -1.5*am, 1.5*am])
        plt.ylabel("Geometrical Illustration of the SVD",
                 fontsize=14).set_weight('bold')
        plt.title("A unit vector, indicated by the red arrow, is multiplied "
                "by\n%s\n to form a blue dot." % self.M, fontsize=10)
        plt.xlabel("Click and drag the tip of "
                 "the red arrow.").set_style("italic")
        plt.show()

    def plot_tf(self):
        self.add_patch(plt.Circle(np.dot(self.M, np.array(self.cp.pos)),
                                0.01))

demo = SVD_Geometry(np.array([[0.7, 1.4], [1.2, 0.1]]))

