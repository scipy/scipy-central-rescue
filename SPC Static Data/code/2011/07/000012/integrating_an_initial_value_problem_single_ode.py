import numpy as np
from scipy import integrate
from matplotlib.pylab import *
 
def tank(t, y):
    """
    Dynamic balance for the chemical reactor (stirred tank)
 
    C_A = y[0] = the concentration of A in the tank, mol/L
 
    Returns dy/dt = F/V*(C_{A,in} - C_A) - k*C_A^2
    """
    F = 20.1     # L/min
    CA_in = 2.5  # mol/L
    V = 100      # L
    k = 0.15     # L/(mol.min)
 
    # Assign some variables for convenience of notation
    CA = y[0]
 
    # Output from this ODE function must be a COLUMN vector, with n rows
    n = len(y) 
    dydt = np.zeros((n,1))
    dydt[0] = F/V*(CA_in - CA) - k*CA**2
    return dydt
 
# The "driver" that will integrate the ODE(s):
# -----------
# Start by specifying the integrator:
# use ``vode`` with "backward differentiation formula"
r = integrate.ode(tank).set_integrator('vode', method='bdf')

# Set the time range
t_start = 0.0
t_final = 10.0
delta_t = 0.1
# Number of time steps: 1 extra for initial condition
num_steps = np.floor((t_final - t_start)/delta_t) + 1

# Set initial condition(s): for integrating variable and time!
CA_t_zero = 0.5
r.set_initial_value([CA_t_zero], t_start)

# Create vectors to store trajectories
t = np.zeros((num_steps, 1))
CA = np.zeros((num_steps, 1))
t[0] = t_start
CA[0] = CA_t_zero

# Integrate the ODE(s) across each delta_t timestep
k = 1
while r.successful() and k < num_steps:
    r.integrate(r.t + delta_t)

    # Store the results to plot later
    t[k] = r.t
    CA[k] = r.y[0]
    k += 1

# All done!  Plot the trajectories:
plot(t, CA)
grid('on')
xlabel('Time [minutes]')
ylabel('Concentration [mol/L]')