'''
@file: coefs_io.py
@author: Anthony White and Kili Miyamoto
@date: 22/03/2023
@brief: Functions related to generating output based on Polygonal Fourier Descriptors (PFDs)
'''

# Import dependancies
from msvcrt import kbhit
from tkinter import S
import numpy as np
#import scipy as sp
import matplotlib.pyplot as plt
from pynverse_modified.inverse import inversefunc
import functools as ft
import math

# Complex polygon basis function
poly_func = lambda k, N, t : np.exp(1j*2*np.pi*k/N*np.floor(N*t))*(1+(np.exp(1j*2*np.pi*k/N)-1)*(N*t-np.floor(N*t)))
poly_func_derivative = lambda k, N, m : N * np.exp(1j*2*np.pi*k*m/N) * (np.exp(1j*2*np.pi*k/N)-1)
#poly_func_derivative = lambda k, N, tpoints : N * np.exp(1j*2*np.pi*k/N*np.floor(N*tpoints)) * (np.exp(1j*2*np.pi*k/N)-1)

def polygon_plot(tpoints, coefs):
    N = coefs.size
    zpoints = np.zeros(tpoints.size, dtype=np.complex_)
    for k in range(0, N):
        zpoints += 1/N*coefs[k]*poly_func(k, N, tpoints)
    return zpoints

def removing_redundant_using_sinc(coefs, M, p):
    '''Function to remove redundant points of PFD

    args:
        coefs : input numpy array of coefs from 0 to N-1
        M : The number of essential vertices
        p : A number from 0 to M-1, any number will give the same results 
        

    returns:
        new_coefs : Cleaned coefficients array 
    
    '''

    N = coefs.size 
    new_coefs = np.zeros(M, dtype=np.complex_) 

    #First cleaned coefficients is always the derived from the first coefficient
    new_coefs[0] = (M/N) * coefs[0]

    for m in range(1, M):
        new_coefs[m] = ((M*(np.sinc((p*M+m)/N)**2))/(N*(np.sinc((p*M+m)/M)**2)))*coefs[p*M+m]


    return new_coefs


def building_block_plot(tpoints, coefs):
    '''Function to plot the sub-polygons that make up the final shape.

    args:
        tpoints : t parameter input to the Fourier series function
        coefs : input numpy array of coefs from 0 to N-1
        

    returns:
        Plots of all the sub-polygons in 2 rows where the first row is coefficients from 1 to N/2 and the second row is coefficients from N to N/2+1. 
        Note the second row plots the sub-polygons in a backwards order for easier comparison.
    
    '''

    N = coefs.size
    half_way = int(N/2)                      #when N is odd the half way value is rounded down
    figure, axis = plt.subplots(2, half_way) #create 2 rows and N/2 columns for subplots. When N is even the bottom left subplot will be empty 
                                             #since the first coefficient contains information on the location and is skipped

    for k in range(1, N):                             #skip first coefficients
        shape = 1/N*coefs[k]*poly_func(k, N, tpoints) #find the sub-polygon shape using poly_func and multiply by 1/N and coefficients for the magnitude

        if((k-1) < half_way):                         # (k-1) so that the half_way point is included in the first row
            axis[0, k-1].plot(np.real(shape), np.imag(shape))
            axis[0, k-1].set_aspect('equal')          #set the aspect ratio to equal so the plots are not distorted
        else:
            axis[1, N-k-1].plot(np.real(shape), np.imag(shape))
            axis[1, N-k-1].set_aspect('equal')

    plt.show()

def poly_area(zpoints):
    '''find the area of a shape by applying the shoelace formula to the array of points 

    args:
        zpoints : input numpy array of the points that make up the shape

    returns:
        area value
    
    '''

    x = np.real(zpoints)    #split array of points into x and y coordinates 
    y = np.imag(zpoints)
    #x = np.flip(x)         #shoelace formula is typically done to points ordered in a anti-clockwise manner but i found no difference so leaving
    #y = np.flip(y)         #this as a comment
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))  #shoelace formula


def area(coefs):
    '''find the area of a shape by applying the formula found through Green's Theorem 

    args:
        coefs : input numpy array of coefs from 0 to N-1

    returns:
        area value
    
    '''


    N = len(coefs)
    area = 0
    for k in range(N):
        area += np.abs(coefs[k])**2*np.sin(2*np.pi*k/N)
    area = area /(2*N)
    return np.abs(area)

def poly_scale(coefs, new_coefs):
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
    new_coefs[0] = coefs[0]
    
    return new_coefs

def low_pass(coefs, att):
    '''Function to apply a low_pass filter to the coefficients

    args:
        coefs : input numpy array of coefs from 0 to N-1
        att : specifies attenutaion of filter
        

    returns:
        new_coefs : numpy array of filtered coefs
    
    '''

    nsize = coefs.size          #find the coefficient array size
    half_way = int(nsize/2)     #when nsize is odd the half way value is rounded down
    new_coefs = np.zeros(nsize, dtype=np.complex_)  #initialise and specify its type

    for k in range(0, nsize):     
        if((k-1) < half_way):   #(k-1) to include the halfway point
            new_coefs[k] = coefs[k] / (1 + att * k)
        else:                   #since after the half way point the coefficient frequency starts decreasing make sure the filtering matches this
            new_coefs[k] = coefs[k] / (1 + att * (nsize - k))

    return new_coefs

def check_collinearity(v0, v1, v2):
    ''' Checks collinearity of three input points (v0, v1, v2), represented in complex coordinate form. Returns 1 if v1 is collinear
    with v0 and v2. Returns 0 otherwise.
    '''
    m1 = np.imag(v1-v0) / np.real(v1-v0)
    m2 = np.imag(v2-v1) / np.real(v2-v1)
    tol = 0.1 * (m1 + m2) / 2 + 0.01
    
    if (tol > 0):
        return (m1-tol <= m2 <= m1+tol)
    else:
        return (m1+tol <= m2 <= m1-tol)

def remove_collinear_points(coefs):
    ''' Removes all PFDs correspoding to collinear vertices from an input array of PFDs

    args:
        coefs : numpy array of PFDs for original shape

    returns:
        new_coefs : numpy array of PFDs for shape with collinear vertices removed

    '''

    # Initialise array of indexes of collinear points
    iscollinear_index = []

    # Determine complex coordinates of vertices from FDs
    vertices = np.fft.ifft(coefs)

    # Check collinearity of first vertex
    if check_collinearity(vertices[vertices.size-1], vertices[0], vertices[1]):
        iscollinear_index.append(0)

    # Check collinearity of all vertices except first and last
    for i in range(1, vertices.size-2):
        if check_collinearity(vertices[i-1], vertices[i], vertices[i+1]):
            iscollinear_index.append(i)

    # Check collinearity of last vertex
    if check_collinearity(vertices[vertices.size-2], vertices[vertices.size-1], vertices[0]):
        iscollinear_index.append(vertices.size-1)
    
    # Delete the collinear vertices and determine new coefs
    new_vertices = np.delete(vertices, iscollinear_index)
    new_coefs = np.fft.fft(new_vertices)
    
    return new_coefs
       
def average(coefs, num):
    '''Reduces the number of FDs via the FD averaging method

    args:
        coefs : numpy array of FDs
        num : number of FDs to average to

    returns:
        nwe_coefs : numpy array of averaged FDs
    '''

    new_coefs = np.array([])
    for i in range(num):
        subset = coefs[i::num]
        amean = subset.sum() / len(subset)
        new_coefs = np.append(new_coefs, amean)
    return new_coefs

def inverse_sinc(coefs, M):
    new_coefs = np.zeros(M, dtype = np.complex_)
    coefs = coefs/coefs.size
    for m in range(0, M):
        new_coefs[m] = (M*np.sinc(m/coefs.size)**2 / np.sinc(m/M)**2) * coefs[m]
    return new_coefs

def start_shift(zpoints, shift):
    '''Shifts the starting point of a set of z values

    args:
        zpoints : numpy array of z values
        shift : integer indicating where the new start point should be
    
    returns:
    new_zpoints : numpy array of z values with different starting point
    
    '''
    new_zpoints = np.concatenate(((zpoints[shift:], zpoints[:shift])))
    return new_zpoints

def get_speed(m, coefs):
    N = len(coefs)
    speed = 1/N * np.abs(np.sum(coefs * poly_func_derivative(np.arange(N), N, m)))
    return speed

def t_param(spoints, coefs):
    '''Solve the inverse function t(s) for s parameterisation

    args:
        spoints = numpy array of input s-values
        coefs = numpy array of PFDs
    
    returns:
        tpoints = numpy array of output t-values
    '''

    # Initialise parameters
    N = len(coefs)
    tpoints = np.zeros(len(spoints))
    m=0
    i=0
    speed = get_speed(0, coefs)
    speed_sum = 0

    while i < len(spoints):

        # Calculate the t-points
        tpoints[i] = spoints[i]/speed if m == 0 else spoints[i]/speed -  speed_sum/(N*speed) + m/N

        # Determine the end point of the line segment and begin new line segment
        if tpoints[i] > (m+1)/N:
            m += 1
            speed_sum += speed
            speed = get_speed(m, coefs)
        else:
            i += 1
    
    # Return the result
    return tpoints

def get_perim(coefs):
    '''Determines the perimeter of the shape from the FDs.

    args:
        coefs : numpy array of FDs

    returns:
        perim : shape perimeter
    '''

    N = len(coefs)
    speed_sum = 0
    for i in range(N):
        speed_sum += get_speed(i, coefs)
    perim = speed_sum /  N
    return perim

