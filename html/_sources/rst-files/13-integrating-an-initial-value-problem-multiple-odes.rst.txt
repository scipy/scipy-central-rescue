Integrating an initial value problem (multiple ODEs)
====================================================

**Author:** scipy-central

**Submitted on:** 2011-07-22 16:52:38-07:00

We extend the example from http://scpyce.org/12/ here to integrate 2 coupled ODEs and include several algebraic equations.

Consider a chemical reactor with a second order reaction :math:`{\sf A} \rightarrow {\sf B}`. Our aim is calculate the concentration,  :math:`C_{\sf A}(t)`, and tank temperature, :math:`T(t)`, as functions of time using an ODE integrator.

We know the reaction rate is :math:`r = k C_{\sf A}^2`, and is an algebraic function of temperature: :math:`k = 0.15 e^{- E_a/(RT)}` L/(mol.min). Furthermore, the reaction is known to release heat, with :math:`\Delta H_r = -590` J/mol.  The time-dependent mass and energy balance for this system can be derived:

.. math:: 
    \frac{dC_{\sf A}(t)}{dt} &= \frac{F(t)}{V} \bigg( C_{{\sf A},\text{in}} - C_{\sf A} \bigg) - 0.15 e^{- E_a/(RT)} C_{\sf A}^2 \\
    \frac{dT(t)}{dt} &= \frac{F(t)\rho C_p(T)}{V \rho C_p(T)}\bigg(T_\text{in} - T(t) \bigg) - \frac{0.15 e^{- E_a/(RT)} C_{\sf A}^2 V (\Delta H_r)}{V \rho C_p}

Notice that these are coupled ODEs, as the first ODE is a function of :math:`T(t)`, while the second ODE is a function of :math:`C_{\sf A}(t)`.
We also know that:

* :math:`C_{{\sf A},\text{in}} = 2.5` mol/L,
* :math:`T_\text{in} = 288` K
* a constant volume of :math:`V = 100` L
* constant inlet flow of :math:`F(t) = 20.1` L/min, though we could easily make it a function of time and adjust the function ``tank`` to use the time variable, ``t``
* molar heat capacity is a weak function of the system temperature: :math:`C_p(T) = 4.184 - 0.002(T-273)` J/(kg.K),
* liquid phase density is :math:`\rho=1.05` kg/L.
* :math:`E_a = 5000` J/mol
* :math:`R = 8.314` J/(mol.K),

We need two initial conditions, one for each of the ODEs:

* :math:`C_{\sf A}(t=0) = 0.5` mol/L
* :math:`T(t=0) = 295` K

In the code we will integrate the ODE from :math:`t_\text{start} = 0.0` minutes up to :math:`t_\text{final} = 45.0` minutes
and plot the time-varying trajectories of temperature and concentration in the tank using ``matplotlib``.

Read the `SciPy documentation <http://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.ode.html>`_ for ``ode``.


.. literalinclude:: /Data/code/2011/07/000013/integrating_an_initial_value_problem_multiple_odes.py
	:language: python

