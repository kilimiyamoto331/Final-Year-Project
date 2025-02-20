'''
@file: fourier_plot.py
@author: Anthony White and Kili Miyamoto
@date: 10/03/2023
@brief: Executable code to conduct research and testing into plotting shapes using the Fourier series
'''

# Import dependancies
import numpy as np
import data_io as io
import polygon_animate as polani

tpoints = lambda num : np.arange(num) / num
noise = lambda num : num * np.random.rand() * np.exp(1j * np.random.rand() * 2 * np.pi)

#A code that simply creates an animation for the 5-sided shape used in our poster.

def main_poster_basis():


    vertices =  io.get_vertices('5-sided.png')

    T = vertices.size * 10

    coefs = np.fft.fft(vertices)
                   
    polani.make_animation(coefs, 'poster_polygon_example.mp4')

if __name__ == '__main__':
    main_poster_basis()

