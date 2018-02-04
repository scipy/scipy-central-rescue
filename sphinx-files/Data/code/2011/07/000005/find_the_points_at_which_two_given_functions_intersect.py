from scipy.optimize import fsolve
import numpy as np

def f(input_vector):
   x, y = input_vector
   return  np.array([y - x**2, y - x - 1.0])


# Solve the function, using (x=1, y=2) as the initial guess
fsolve(f, [1.0, 2.0])