'''
@file: fourier_N_alter.py
@author: Anthony White and Kili Miyamoto
@date: 10/03/2023
@brief: Genrates a plot of a 2D object using complex Fourier series coeffiecients located in fourier_coefficients.csv
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

    # Prompt user to select option
    pattern = int(input('Select pattern: '))

    # Extract Fourier coefficients from .csv data
    pattern_data = data[pattern]

    # Print Fourier coefficients and extract coefficients from the data
    print("\nFourier Coeffiecients:")
    coefs = []
    for coef in pattern_data[1:]:
        if coef:
            coefs.append(coef)
            print(coef)

    # Add a 0 to the Fourier coefficients if there is an even number of elements
    if not len(coefs) % 2:
        coefs.append(0)

    # Convert to a numpy array
    coefs = np.array(coefs, dtype=np.complex_)

    return coefs

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
    coefs = get_coefs()


    # Prompt user to input maximum N values and convert the string to an interger array
    string_N = input('\nEnter maximum N value, split each input using a comma:')
    string_N = string_N.split(',')
    array_N = [int(numeric_string) for numeric_string in string_N]

    
    tpoints = []
    # Create multiple arrays of 't' values
    for i in range(len(array_N)):
        tpoints.append(np.linspace(start=0, stop=1, num=array_N[i]))

    # Calculate output using the Fourier series
    fourier_func_arr = np.vectorize(fourier_func, excluded=coefs)

    zpoints = []

    # Cralculate z points using each array of t values
    for j in range(len(tpoints)):
        zpoints.append(fourier_func_arr(coefs, tpoints[j]))

    # Plot the output
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.set_aspect('equal')
    
    plt.xlabel('x')
    plt.ylabel('y')
    for j in range(len(tpoints)):
        fig = plt.figure(j)
        plt.scatter(np.real(zpoints[j]), np.imag(zpoints[j]))
    plt.show()

# Boiler plate guard for main()
if __name__ == "__main__":
    main()
