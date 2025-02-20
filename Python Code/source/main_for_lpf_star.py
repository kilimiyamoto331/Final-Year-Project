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
import polygon_animate as polani

tpoints = lambda num : np.arange(num) / num

#There are two parts to this code the first part is the plotting of a shape before and after low pass filtering, the second part is creating an animation to 
#demonstrate how the collinear points are creating redundant PFDs and the use of the cleaning function to remove/correct the PFDs. 
#When you run the code a separate window with the plot will show up and closing this window will initiate the second part. The animations will be generated in 
#whatever folder this code is in. If you wish to play around with the code and want to skip the generation of the animation to save time add a # before code
#just like how this comment has been created.

def main_for_lpf_star():

    vertices =  io.get_vertices('star.png')                             #Get the vertice coordinates from an image of a star

    coefs = np.fft.fft(vertices)                                        #PFD of the star
    fil_coefs = pol.low_pass(coefs, 10)                                 #Low pass filter the star PFD.
                                                                        #Feel free to increase the value on the right, it will have no further effect on the shape

    fil_coefs = pol.poly_scale(coefs, fil_coefs)                        #Scale the filtered coefficient to the original star PFD using the area ratio

    T = 100                                                             #Set the number of points to an arbitrary high number that is a multiple of the number of PFD. 
                                                                        #This is to make sure when drawing the shape the essential vertices are captured.

    zpoints = pol.polygon_plot(tpoints(T), coefs)                       #Plot the star
    fil_zpoints = pol.polygon_plot(tpoints(T), fil_coefs)               #Plot the filtered star

    gui.create_window(zpoints, coefs, fil_zpoints, fil_coefs)           #Show the plot overlapped with each other

    polani.make_animation(fil_coefs, 'Redundant_PFD_example.mp4')       #Make animation of pentagon with redundant PFD, specifying the name of the mp4

    cleaned_coefs = pol.removing_redundant_using_sinc(fil_coefs, 5, 0)  #Clean the PFD

    polani.make_animation(cleaned_coefs, 'Clean_PFD_example.mp4')       #Make animation of pentagon with clean PFD, specifying the name of the mp4

if __name__ == '__main__':
    main_for_lpf_star()

