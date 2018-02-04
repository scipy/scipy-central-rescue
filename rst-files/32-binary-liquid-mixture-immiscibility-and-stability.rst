Binary Liquid Mixture Immiscibility and Stability 
==================================================

**Author:** keitho

**Submitted on:** 2011-11-19 10:17:37-08:00

Determines regions of immiscibility and any limits of essential instability for a binary liquid mixture of components B and C. the excess Gibbs energy of mixing is given explicitly by an empirical equation: 

\(\Delta G^{ex}/RT = x_{B}x_{C}[k_{1}+k_{2}(x_{B}-x_{C})+k_{3}(x_{B}-x_{C})^2]\)

where \(x_{B}+x_{C} = 1\)

The essential one-phase instability is between the orange points (spinodal points).
The region of immiscibility is between the red points (binodal points).
Blue points show the minima, which are not equal to the binodal points.

.. image:: /Data/media/images/201111/plot3.png

.. literalinclude:: /Data/code/2011/11/000032/binary_liquid_mixture_immiscibility_and_stability.py
	:language: python

