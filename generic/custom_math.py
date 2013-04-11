# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

#TODO move some more stuff from utils.py here

from math import log10, floor

import numpy as np
from numpy.core.umath_tests import matrix_multiply as mmultr

def mmult(A, B):
    return np.sum(np.transpose(A,(0,2,1))[:,:,:,np.newaxis]*B[:,:,np.newaxis,:],-3)
    
def mdot(A,B):
    C = np.zeros(shape=A.shape, dtype=np.complex)
    for i in range(A.shape[0]):
        C[i] = np.dot(A[i], B[i])
    return C
    
def mtim(A,B):
    C = np.zeros(shape=A.shape, dtype=np.complex)
    for i in range(A.shape[0]):
        C[i] = np.multiply(A[i], B[i])
    return C
        
    
def solve_division(A,B):
    bt = np.transpose(B, axes=(0,2,1))
    at = np.transpose(A, axes=(0,2,1))
    return np.array([np.transpose(np.linalg.lstsq(bt[i], at[i])[0]) for i in range(bt.shape[0])])
    
def round_sig(x, sig=1):
    if x == 0:
        return 0
    else:
        return round(x, sig-int(floor(log10(abs(x))))-1)
