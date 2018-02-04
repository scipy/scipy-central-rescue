Integrating an initial value problem (single ODE)
=================================================

**Author:** scipy-central

**Submitted on:** 2011-07-22 05:01:45-07:00

We want to integrate a single equation :math:`\displaystyle \frac{dy(t)}{dt} = f(t, y)` with a given initial condition :math:`y(t=0)=y_0`.

There are several integrators available in SciPy.  This tutorial uses the `VODE integrator <https://computation.llnl.gov/casc/nsde/pubs/207532.pdf>`_. It is a good general-purpose solver for both stiff and non-stiff systems.

The example is a common modelling reaction: a liquid-based stirred tank reactor, with (initially) constant physical properties, a second order chemical reaction where species A is converted to B according to  :math:`{\sf A} \rightarrow {\sf B}`, with reaction rate :math:`r = k C_{\sf A}^2`.  One can find the time-dependent mass balance for this system to be:

.. math::

    \frac{dC_{\sf A}(t)}{dt} = \frac{F(t)}{V} \bigg( C_{{\sf A},\text{in}} - C_{\sf A} \bigg) - k C_{\sf A}^2

where 

* :math:`C_{{\sf A},\text{in}} = 5.5` mol/L, 
* we will initially assume constant volume of :math:`V = 100` L 
* constant inlet flow of :math:`F(t) = 20.1` L/min, and
* a reaction rate constant of :math:`k = 0.15 \frac{\text{L}}{\text{mol}.\text{min}}`.  

We must specify an initial condition for each differential equation: we will assume :math:`C_{\sf A}(t=0) = 0.5` mol/L. 

In the code we integrate the ODE from :math:`t_\text{start} = 0.0` minutes up to :math:`t_\text{final} = 10.0` minutes and plot the time-varying trajectory of concentration in the tank using ``matplotlib``. The plot shows the reactor starts with a concentration of :math:`C_{\sf A}(t=0) = 0.5` mol/L and reaches a steady state value of about :math:`C_{\sf A}(t=\infty) = 1.28` mol/L.

Read the `SciPy documentation <http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.ode.html>`_ for ``ode``.


.. literalinclude:: /Data/code/2011/07/000012/integrating_an_initial_value_problem_single_ode.py
	:language: python

