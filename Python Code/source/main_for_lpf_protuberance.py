'''
@file: fourier_plot.py
@author: Anthony White and Kili Miyamoto
@date: 10/03/2023
@brief: Executable code to conduct research and testing into plotting shapes using the Fourier series
'''

# Import dependancies
import numpy as np
import gui
import data_io as io
import fourier as fr

tpoints = lambda num : np.arange(num) / num

#A simple code showing the low pass filtering outcome for a Circular FD

def main_for_lpf_protuberance():

    data = io.get_csv_data()                                    #Read a set of shapes from a csv file
    coefs = io.get_coefs_manual(data, 15)                       #obtain the FD of the protuberance shape
    fil_coefs = fr.low_pass(coefs, 1)                           #Low pass filter the protuberance FD
    fil_coefs = fr.scale(coefs, fil_coefs)                      #Scale the filtered coefficient to the original protuberance FD using the area ratio

    T = 100                                                     #Set the number of points to plot 

    zpoints = fr.fourier_plot(tpoints(T), coefs)                #Plot the protuberance
    fil_zpoints = fr.fourier_plot(tpoints(T), fil_coefs)        #Plot the filtered protuberance

    gui.create_window(zpoints, coefs, fil_zpoints, fil_coefs)   #Show the plot overlapped with each other

if __name__ == '__main__':
    main_for_lpf_protuberance()

