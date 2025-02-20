'''
@file: coefs_io.py
@author: Anthony White and Kili Miyamoto
@date: 22/03/2023
@brief: Functions handling input and output of Fourier coefficients.
'''

# Import dependancies
import numpy as np
import csv
import cv2 as cv
from shapely.geometry import LineString
from shapely.ops import unary_union

def get_csv_data():
    '''Function to extract data from the file fourier_coeffiecients.csv

    returns:
        data : a 2D list of strings extracted from fourier_coeffiecients.csv

    '''

    # Open and read the .csv file and convert data to a list
    with open('fourier_coefficients.csv', mode='r', encoding='utf-8') as file:
        data = list(csv.reader(file, delimiter=','))

    return data

def print_patterns(data):
    '''Function to print pattern options to the console from the .csv data

    args:
        data : a 2D list of strings extracted from fourier_coeffiecients.csv

    '''

    # Print pattern options
    for row in data:
        print(f'{data.index(row)} - {row[0]}')

def get_coefs(data, n=''):
    '''Function to prompt user from the console to select a pattern and return a numpy array of
    fourier coeffeicients based on user selection and data in fourier_coeffiecients.csv.

    args:
        data : a 2D list of strings extracted from fourier_coeffiecients.csv
        n : (optional) pattern number printed in the input prompt
    
    returns:
        coefs : a numpy array of Fourier descriptors
    
    '''

    # Prompt user to select option
    pattern = int(input(f'Select pattern {n}: '))

    # Extract pattern data from .csv data
    pattern_data = data[pattern]
    coefs = []
    [coefs.append(coef) for coef in pattern_data[1:] if coef]

    # Convert to a numpy array
    coefs = np.array(coefs, dtype=np.complex_)

    return coefs

def get_coefs_manual(data, n):
    '''Function to prompt user from the console to select a pattern and return a numpy array of
    fourier coeffeicients based on user selection and data in fourier_coeffiecients.csv.

    args:
        data : a 2D list of strings extracted from fourier_coeffiecients.csv
        n : (optional) pattern number printed in the input prompt
    
    returns:
        coefs : a numpy array of Fourier descriptors
    
    '''

    # Prompt user to select option
    pattern = int(n)

    # Extract pattern data from .csv data
    pattern_data = data[pattern]
    coefs = []
    [coefs.append(coef) for coef in pattern_data[1:] if coef]

    # Convert to a numpy array
    coefs = np.array(coefs, dtype=np.complex_)

    return coefs

def print_coefs(coefs, n=''):
    '''Function to print Fourier coefficients to the console.

    args:
        coefs : a numpy array of Fourier descriptors
        n : (optional) pattern number printed in the output

    '''
    print(f'\nFourier Coefficients {n}:')
    [print(coef) for coef in coefs]

def get_boundary(filename, num_points):
    '''Function to extract position values of points evenly spaced along a shape boundary from a 
    greyscale image. Pixels with intensity values 0-127 are considered the background of the shape and
    pixels with intensity values 128-255 are considered the foreground of the shape.

    args:
        filename : filename of the image containing the shape
        num_points : number of points along shape boundary to return

    returns:
        zpoints : numpy array of position values representing points evenly spaced along shape boundary
    
    '''

    # Read the image and convert to greyscale
    image = cv.imread(filename)
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Define a threshold of intensity values. 0-127 for background and 128-255 for foreground
    thresh = cv.threshold(image_gray, 127, 255, 0)[1]

    # Find the coordinates of points on the shape boundary
    contour = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[0][0]

    # Reformat the contour into a list of tuples
    new_contour = []
    [new_contour.append(tuple(point[0])) for point in contour]

    # Create a LineString object from the contour points
    line = LineString(new_contour)

    # Determine coordinates of points evenly spaced along the boundary
    distances = np.linspace(0, line.length, num_points+1)[:-1]
    points = [line.interpolate(distance).coords[:] for distance in distances]

    # Reformat the points into a numpy array of complex position values
    zpoints = np.array([], dtype = np.complex_)
    for point in points:
        zpoints = np.append(zpoints, point[0][0] - 1j*point[0][1])
    
    return zpoints

def get_vertices(filename):
    '''Function to extract position values of vertices along a shape boundary from a 
    greyscale image. Pixels with intensity values 0-127 are considered the background of the shape and
    pixels with intensity values 128-255 are considered the foreground of the shape.

    args:
        filename : filename of the image containing the shape

    returns:
        vertices : numpy array of vertices in complex coordinate form along shape boundary
    
    '''

    # Read the image and convert to greyscale
    image = cv.imread(filename)
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Define a threshold of intensity values. 0-127 for background and 128-255 for foreground
    thresh = cv.threshold(image_gray, 127, 255, 0)[1]

    # Find the coordinates of points on the shape boundary
    contour = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)[0][0]

    # Extract vertices
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)

    # Convert to complex coordinate form
    vertices = np.array([], dtype = np.complex_)
    for point in approx:
        vertices = np.append(vertices, point[0][0] -1j*point[0][1])

    return vertices



