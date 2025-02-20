'''
@file: fourier_compare.py
@author: Anthony White
@date: 10/03/2023
@brief: Generates a two overlapping plot of a 2D object using complex Fourier series coeffiecients located in fourier_coefficients.csv
'''

# Import dependancies
import csv
import matplotlib.pyplot as plt
import numpy as np

def get_coefs():
    '''Function to prompt user to select a pattern and extract Fourier coefficients from the .csv file

    returns:
        coefs : numpy array of Fourier coeffients
    '''

    # Open and read the .csv file and convert data to a list
    with open('fourier_coefficients.csv', mode='r', encoding='utf-8') as file:
        data = list(csv.reader(file, delimiter=','))

    # Print pattern options
    for row in data:
        print(f"{data.index(row)} - {row[0]}")

    # Prompt user to select option for first pattern
    pattern = int(input('Select pattern 1: '))

    # Prompt user to select option for second pattern
    pattern2 = int(input('Select pattern 2: '))

    # Extract Fourier coefficients from .csv data
    pattern_data = [data[pattern], data[pattern2]]

    


   # coefs3 = np.array([pattern_data[0][1:], pattern_data[1][1:]], axis=0)




    
    # Extract coefficients from the data
    coefs = []
    for coef in pattern_data[0][1:]:
        if coef:
            coefs.append(coef)
            
    coefs2 = []
    for coef in pattern_data[1][1:]:
        if coef:
            coefs2.append(coef)
    
    

    
 
    # Add a 0 to the Fourier coefficients if there is an even number of elements
    if not len(coefs) % 2:
        coefs[0].append(0)

    if not len(coefs2) % 2:
        coefs[1].append(0)

    # Convert to a numpy array
    coefs = np.array(coefs, dtype=np.complex_)
    coefs2 = np.array(coefs2, dtype=np.complex_)

    return coefs, coefs2

def fourier_func(coefs, tpoint):
    '''Function to implement Fourier series function based on Fourier coefficients

    args:
        coefs : numpy array of Fourier coeffients
        tpoint : input to the Fourier series function

    returns:
        zpoint : output of the Fourier series function
    '''

    # Determine index of c0
    m = int(coefs.size/2)

    # Add complex exponential Fourier terms
    zpoint = 0
    for n in range(-m, m + 1):
        zpoint += coefs[n + m] * np.exp(1j*2*np.pi*n*tpoint)

    return zpoint

def main():
    '''Main program
    '''

    # Create array of Fourier coefficients
    two_coefs = get_coefs()

    # Create array of 't' values
    tpoints = np.linspace(start=0, stop=1, num=100)

    # Calculate output using the Fourier series
    fourier_func_arr = np.vectorize(fourier_func, excluded=two_coefs[0])
    zpoints = fourier_func_arr(two_coefs[0], tpoints)
    fourier_func_arr = np.vectorize(fourier_func, excluded=two_coefs[1])
    zpoints2 = fourier_func_arr(two_coefs[1], tpoints)

    # Plot the output
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.scatter(np.real(zpoints), np.imag(zpoints))
    plt.scatter(np.real(zpoints2), np.imag(zpoints2))
    plt.show()

# Boiler plate guard for main()
if __name__ == "__main__":
    main()
