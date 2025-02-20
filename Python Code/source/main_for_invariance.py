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
import polygon as pol

tpoints = lambda num : np.arange(num) / num

#Code to test if the invariance properties work with PFDs. By altering the three variables scale, rotate and translate we can test if the PFD is truly
#invariant to any manipulation.

def main_for_invariance():

    vertices =  io.get_vertices('star.png')                                     #Get the vertice coordinates from an image of a star
    coefs = np.fft.fft(vertices)                                                #PFD of the star

                                                                                #Feel free to change the following three variables to anything reasonable
    scale = 2                                                                   #Scaling factor
    rotate = np.pi/2                                                            #Rotation factor
    translate = 1+1j                                                            #Complex coordinates of the origin


    manipulated_coefs = scale*coefs*np.exp(1j*rotate)                           #Apply the scaling and rotation factor to the PFD
    manipulated_coefs[0] = translate                                            #Translate the PFD 

    coefs = np.abs(coefs)                                                       #Convert the complex PFD values to absolute values for rotational invariance
    manipulated_coefs = np.abs(manipulated_coefs)

    coefs = coefs/coefs[1]                                                      #Scale all PFD values by the first PFD for scale invariance
    manipulated_coefs = manipulated_coefs/manipulated_coefs[1]

    coefs[0] = 0                                                                #Set the origin to 0+0j for translation invariance
    manipulated_coefs[0] = 0


    T = 100                                                                     #Set the number of points to an arbitrary high number that is a multiple of the number of PFD. 
                                                                                #This is to make sure when drawing the shape the essential vertices are captured.

    zpoints = pol.polygon_plot(tpoints(T), coefs)                               #Plot the star with invariant PFD
    manipulated_zpoints = pol.polygon_plot(tpoints(T), manipulated_coefs)       #Plot the star with manipulated invariant PFD

    gui.create_window(zpoints, coefs, manipulated_zpoints, manipulated_coefs)   #Show the plot overlapped with each other
    
if __name__ == '__main__':
    main_for_invariance()

