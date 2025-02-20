'''
@file: fourier_pop.py
@author: Anthony White & Kili Miyamoto
@date: 10/03/2023
@brief: Genrates a plot of a 2D object using complex Fourier series coeffiecients located in fourier_coefficients.csv and prompts user 
        to enter y to remove the highest order coefficient to replot
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
    #if not len(coefs) % 2:
    #    coefs.append(0)
    '''
    i have removed this function and edited the fourier func loop to work without it
    this is because when removing indivisual coefficients the appended zero will get
    in the way 
    '''




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
    for n in range(-m, -m + coefs.size - 1):
        zpoint += coefs[n + m] * np.exp(1j*2*np.pi*n*tpoint)

    return zpoint








def delete_coef(coefs):
    '''Function to delete highest order Fourier coefficient

    args:
        coefs : numpy array of Fourier coeffients

    returns:
        coefs : numpy array of Fourier coeffients
    '''
    # Determine index of c0
    m = int(coefs.size/2)

    #if the highest positive n value is larger than or equal to the lowest negative n value then remove the highest positive value. 
    if abs(-m) <= abs(-m + coefs.size - 1):
        coefs = coefs[:coefs.size - 1]
    else:
        coefs = coefs[1:]   

    return coefs





def main():
    '''Main program
    '''

    # Create array of Fourier coefficients
    coefs = get_coefs()

    # Create array of 't' values
    tpoints = np.linspace(start=0, stop=1, num=100)

    

    #Repeat all following functions until break statment
    while (True):

        # Calculate output using the Fourier series
        fourier_func_arr = np.vectorize(fourier_func, excluded=coefs)
        zpoints = fourier_func_arr(coefs, tpoints)

        # Plot the output
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.scatter(np.real(zpoints), np.imag(zpoints))
        plt.show()

        #If only 2 coefficients left removing another coefficient will not create a shape and so exit loop
        if coefs.size == 2:
            print("No more coefficients to remove") 
            break   
            


        #Prompt user to enter y if they wish to remove coefficients, if any other thing is entered exit loop    
        remove = input('Enter ''y'' to remove highest order coefficient: ')
        if remove == 'y':
            coefs = delete_coef(coefs)
        else: 
            break









# Boiler plate guard for main()
if __name__ == "__main__":
    main()
