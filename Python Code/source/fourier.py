'''
@file: coefs_io.py
@author: Anthony White and Kili Miyamoto
@date: 22/03/2023
@brief: Functions related to generating output based on the circular FD representation
'''

# Import dependancies
import numpy as np
import scipy as sp
from pynverse_modified.inverse import inversefunc
import functools as ft
import math

def fourier_plot(tpoints, coefs):
    '''Function to implement Fourier series function based on FDs

    args:
        tpoints : numpy array of inputs to the Fourier series function
        coefs : numpy array of FDs

    returns:
        zpoints : numpy array of outputs of the Fourier series function

    '''

    # Determine index of c0
    m = int(coefs.size/2)

    # Add complex exponential Fourier terms
    zpoints = 0
    for n in range(-m, m + (coefs.size % 2)):
        zpoints += coefs[n + m] * np.exp(1j*2*np.pi*n*tpoints)

    return zpoints

def s_param_integrand(tpoint, coefs):
    '''Function to implement the integrand for the function s(t) used for arc length parameterisation

    args:
        tpoint : t parameter input to the Fourier series function
        coefs : numpy array of FDs

    returns:
        integrand : integrand for s(t)
    
    '''

    # Create array of 'n' values
    nsize = coefs.size
    npoints = np.linspace(0, nsize-1, nsize, dtype=int) - int(nsize/2)

    # Calculate the integrand
    integrand = np.absolute(np.sum(1j*2*np.pi*npoints*coefs*np.exp(1j*2*np.pi*npoints*tpoint)))

    return integrand

def s_param_point(tpoint, coefs):
    '''Function to evaluate the function s(t) to reparameterise a single t value into an s value.

    args:
        tpoint : t parameter input to the Fourier series function
        coefs : numpy array of FDs

    returns:
        spoint : s parameter input to the Fourier series function
    
    '''

    spoint = sp.integrate.quad(s_param_integrand, 0, tpoint, args=(coefs))[0]

    return spoint

def s_param(tpoints, coefs):
    '''Function to evaluate the function s(t) to reparameterise an array of t values into s values.

    args:
        tpoints : numpy array of t parameter inputs to the Fourier series function
        coefs : numpy array of FDs

    returns:
        spoint : numpy array of s parameter inputs to the Fourier series function
    '''

    # Loop through the array of t values, reparameterising each one
    spoints = np.zeros(tpoints.size)
    for i in range(tpoints.size):
        spoints[i] = s_param_point(tpoints[i], coefs)
    
    return spoints

def fsolve_func(spoint, coefs):
    return (s_param_point(spoint, coefs) - spoint)

def t_param_point(spoint, coefs):
    '''Function to evaluate the inverse of s(t) to reparameterise a single s value into an t value.

    args:
        spoint : s parameter input to the Fourier series function
        coefs : numpy array of FDs

    returns:
        tpoint : t parameter input to the Fourier series function
    
    '''

    '''
    s0 = spoint/perim_from_coefs(coefs)
    tpoint, = sp.optimize.fsolve(fsolve_func, s0, args=coefs)
    print(tpoint)
    '''

    tpoint = inversefunc(ft.partial(s_param_point, coefs=coefs), y_values=spoint)

    return tpoint

def t_param(spoints, coefs):
    '''Function to evaluate the inverse of s(t) to reparameterise an array of s values into t values.

    args:
        spoints : numpy array of s parameter inputs to the Fourier series function
        coefs : numpy array of FDs

    returns:
        tpoint : numpy array of t parameter inputs to the Fourier series function
    
    '''

    tpoints = np.zeros(spoints.size)
    for i in range(spoints.size):
        tpoints[i] = t_param_point(spoints[i], coefs)
    return tpoints

def perim_from_coefs(coefs):
    '''Function to calculate the shape perimeter from the FDs

    args:
        coefs : numpy array of FDs

    returns:
        perim : shape perimeter
    
    '''
    return s_param_point(1, coefs)

def perim_from_z(zpoints):
    '''Function to calculate the shape perimeter from the boundary

    args:
        zpoints : numpy array of points along the shape boundary

    returns:
        perim : shape perimeter
    
    '''
    perim = 0
    zpoints = np.append(zpoints, zpoints[0])
    for i in range(zpoints.size-1):
        perim += np.absolute(zpoints[i] - zpoints[i+1])
    return perim

def get_coefs_from_zpoints(zpoints, N):
    return np.fft.fftshift(np.fft.fft(zpoints))/N

def area(coefs):
    '''Function to calculate the area of a boundary from the corresponding FDs

    args:
        coefs : numpy array of FDs

    returns:
        tpoint : numpy array of t parameter inputs to the Fourier series function
    
    '''
    # Initialise area to zero
    area = 0

    # Determine index of c0
    m = int(coefs.size/2)

    # For each coefficient cn, increment area by pi*|cn|, except for c0
    for n in range(-m, m + (coefs.size % 2)):
        area += n* np.pi * ((np.absolute(coefs[n+m]))**2)

    return np.abs(area)

def scale(coefs, new_coefs):
    '''scale the new set of zpoints using the original set of z points

    args:
        coefs : input numpy array of coefs from 0 to N-1
        new_coefs : input numpy array of the other coefs from 0 to N-1

    returns:
        new_coefs : other coefs scaled
    
    '''

    a1 = area(coefs)        #find the area using the area func of both shapes
    a2 = area(new_coefs)
    scale_factor = a1/a2    #and find the ratio between the two
    
    new_coefs = new_coefs*math.sqrt(scale_factor)  #multiply the new shape by the square root of the ratio found. Square root since both x and
                                                       #y are multiplied

    m = int(coefs.size/2)
    new_coefs[m] = coefs[m]
    
    return new_coefs

def pop(coefs, num_terms):
    '''Function to remove terms from an array of FDs.

    args:
        coefs : input numpy array of coefs either from -N to N or from -N to N-1
        num_terms : number of terms to remove

    returns:
        new_coefs : input numpy array of coefs either from -M to M or from -M to M-1
    
    '''

    for i in range(num_terms):

        # If the array size is odd, remove term from end, otherwise remove term from front
        coefs = np.delete(coefs, coefs.size-1) if (coefs.size % 2) else np.delete(coefs, 0)
    
    return coefs


def low_pass(coefs, att):
    '''Function to apply a low pass filter to an array of FDs, using a 
    transfer function 1 / (1 + att*cn)

    args:
        coefs : input numpy array of coefs
        att : specifies attenutaion of filter

    returns:
        new_coefs : input numpy array of coefs
    
    '''
    nsize = coefs.size
    npoints = np.linspace(0, nsize-1, nsize, dtype=int) - int(nsize/2)
    new_coefs = coefs / (1 + att * np.absolute(npoints))
    return new_coefs
