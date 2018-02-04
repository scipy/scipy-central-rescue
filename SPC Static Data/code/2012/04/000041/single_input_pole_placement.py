# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0

import numpy as np
from numpy import r_, c_
from numpy.linalg import inv


import sympy as sp

"""
This module provides the functionality for calculating a linear feedback
controller which places the poles of the closed loop system at desired
locations in the complex plane

Works for controllable single input systems.

Dependencies: numpy, sympy

tags: pole placement, ackermann's formula, linear feedback control 

"""



s = sp.Symbol('s')


def ev_to_poly(*evalues):
    """
    takes a list of eigenvalues and returns the corresponding
    characteristic polynomial
    """

    p = 1
    for ev in evalues:
         p*=(s-ev)
         
    return p

def new_matrix(A, b):
    """
    takes (n by n) system matrix A and (n by 1) input vector b
    returns: A* : = A-k.T*b
    where k consists of n symbols k1, ..., kn
    """

    n, m = A.shape
    assert n == m
    
    kk = sp.Matrix(sp.symbols('k1:%i' % (n+1)))
    
    return A - b*kk.T, kk

def char_equ(A):
    """
    returns the characteristic equation of the matrix A
    """
    
    n, m = A.shape
    assert n == m
    
    return (sp.eye(n)*s - A).det() 
    


def place(A, b, evalues):
    """
    performes pole placement for the dynamical system given by
        x_dot = A*x + b*u
    by determining a linear feedback law u = -k.T*x

    takes A, b and the disired eigenvalues of the closed loop system
    
    returns the vector k
    """

    des_poly = ev_to_poly(*evalues)
    
    newA, kk = new_matrix(A, b)
    
    poly_eq = sp.Poly(char_equ(newA)-des_poly, s, domain = 'EX')
    
    eqsys = poly_eq.as_dict().values()
    res = sp.solve(eqsys, *list(kk))
    
    return kk.subs(res)
    
def sym_to_num(arr):
    return np.array(list(arr), dtype=np.float).reshape(arr.shape)

def test1():    
    """
    test the algorithm with the inverted pendulum on a cart example
    """

    g = 9.81
    l = 0.5 
    
    # System matrices (input: cart acceleration)
    A = sp.Matrix([0,0,1,0, 0,0,0,1, 0,0,0,0, 0,g/l,0,0]).reshape(4,4)
    b = sp.Matrix([0,0,1,1/l]).reshape(4,1)

    poles1 = r_[-3, -2, -1 +1j, -1-1j]
    kk = place(A, b, poles1)

    # convert from sympy to numpy 
    A_np = sym_to_num(A)
    b_np = sym_to_num(b)
    kk_np = sym_to_num(kk)
    

    A_res = A_np - np.dot(b_np, kk_np.T)
    
    U1,V1 = np.linalg.eig(A_np)
    U2,V2 = np.linalg.eig(A_res)
    
    print "without feedback:", U1, "(unstable)"
    print "with feedback:", U2, "(stable)"
    

if __name__ == '__main__':
    test1()