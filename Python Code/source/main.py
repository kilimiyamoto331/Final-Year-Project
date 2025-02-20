'''
@file: fourier_plot.py
@author: Anthony White and Kili Miyamoto
@date: 10/03/2023
@brief: Executable code to conduct research and testing into plotting shapes using the Fourier series
'''

# Import dependancies
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import gui
import data_io as io
import fourier as fr
import polygon as pol

tpoints = lambda num : np.arange(num) / num
convert_to_db = lambda num : 20*np.log10(num)
convert_from_db = lambda num : 10**(num/20)
noise = lambda num : num * np.random.rand() * np.exp(1j * np.random.rand() * 2 * np.pi)
a = lambda num : np.abs(num)**2

def function(k, N):
    sum = 0
    for i in range(-100000, 100000):
        m = i*N+k
        sum += m * np.sinc(m/N)**4
    return sum

def main():
    '''
    k = np.arange(800)/20
    N=1
    y = function(k, N)
    print(function(N/4, N))
    y2 = np.pi * N / 20 * np.sin(2*np.pi*k/N)
    #plt.plot(k, y, k, y2)
    #plt.show()
    '''



    data = io.get_csv_data()
    io.print_patterns(data)
    coefs = io.get_coefs(data)
    print(fr.area(coefs))
    zpoints = fr.fourier_plot(tpoints(100), coefs)
    gui.create_window(zpoints, coefs)
    plt.plot(tpoints(40), fr.s_param(tpoints(40), coefs))
    plt.show()
    perim = fr.perim_from_z(zpoints)
    spoints = perim * np.arange(100) / 100
    coefs = fr.get_coefs_from_zpoints(zpoints, 100)
    tpoints1 = fr.t_param(spoints, coefs)
    print(tpoints1)
    curvature = fr.curvature(coefs, spoints/perim)
    print(curvature)
    zpoints_new = fr.fourier_plot(tpoints1, coefs)
    coefs_new = fr.get_coefs_from_zpoints(zpoints_new, 100)
    zpoints_newer = fr.fourier_plot(tpoints(100), coefs_new)
    print(fr.area(coefs_new))
    gui.create_window(zpoints_newer, coefs_new)
    zpoints_newest = fr.fourier_plot(fr.s_param(tpoints(100), coefs_new)/perim, coefs_new)
    gui.create_window(zpoints_newest, coefs_new)

    

    '''
    # Quadrilaterals
    vertices = np.array([-5-3j, -4+4j, 6+3j, 2-2j])
    #vertices = np.array([-5-10j, -2+6j, 7+9j, 2-2j])

    # Define the vertices of the shape
    #vertices = np.array([-2-1j, -2+1j, 2+1j, 1.5-1j])

    # Determine the t-parameterised PFDs from the vertices
    coefs = np.fft.fft(vertices)

    #gui.create_window(s, coefs)
    #plt.plot(tpoints(40),s)
    #plt.show()

    # Define linearly spaced s values
    perim = pol.get_perim(coefs)
    spoints = perim * tpoints(100)
    # Evaluate t(s)
    tpoints_new = pol.t_param(spoints, coefs)
    #plt.plot(s, tpoints_new)
    #plt.show()


    # Plot the s-parameterised shape
    zpoints_new = pol.polygon_plot(tpoints_new, coefs)
    coefs_new = np.fft.fft(zpoints_new)
    print(pol.area(coefs))
    print(pol.area(coefs_new))
    gui.create_window(zpoints_new, coefs_new)

    coefs_newer = np.append(coefs_new[:10], coefs_new[90:])
    zpoints_newer = pol.polygon_plot(tpoints(400), coefs_newer)
    gui.create_window(zpoints_newer, coefs_newer)
    '''


    '''
    zpoints1 = -20 + 1j*np.linspace(-10, 10, 21)
    zpoints2 = np.linspace(-19, 19, 39) + 1j*10
    zpoints3 = 20 - 1j*np.linspace(-10, 10, 21)
    zpoints4 = -np.linspace(-19, 19, 39) - 1j*10
    zpoints = np.concatenate((zpoints1, zpoints2, zpoints3, zpoints4))
    '''
    '''
    zpoints1 = -20 + 1j*np.linspace(-10, 10, 26)
    zpoints2 = np.linspace(-20, 20, 26) + 1j*10
    zpoints3 = 20 - 1j*np.linspace(-10, 10, 26)
    zpoints4 = -np.linspace(-20, 20, 26) - 1j*10
    zpoints = np.concatenate((zpoints1, zpoints2[1:25], zpoints3, zpoints4[1:25]))
    coefs = np.fft.fft(zpoints)
    '''

    # Scalene triangle
    #zpoints3 = np.array([-5-2j, 2+5j, 4-1j])
    #zpoints3 = np.array([-4-3j, -5+4j, 4+2j])
    #zpoints6 = np.array([-2-1j, -2+1j, 1j, 2+1j, 2-1j, -1j])
    #coefs6 = np.fft.fft(zpoints6)
    #print(np.abs(coefs6)/6)
    #print((np.abs(coefs6)**2)/36*np.sin(2*np.pi/6))
    #pol.building_block_plot(tpoints(100), coefs6)

    
    
    #zpoints6 = np.array([-5-7j, -10-2j, -5+5j, 2+10j, 4+4j, 5-7j])
    #coefs6 = np.fft.fft(zpoints6)
    #zpoints100 = pol.polygon_plot(tpoints(102), coefs6)
    #for i in range(len(zpoints100)):
        #zpoints100[i] += noise(0.01)
    #coefs100 = np.fft.fft(zpoints100)

    

    #new_coefs = coefs100[0:4]  # Taking first three
    #new_coefs = pol.split_amean(coefs99, 3)  # Split AM
    #new_coefs = pol.split_gmean(coefs99, 3)  # Split GM
    #new_coefs = pol.split_rms(coefs100, 4)  # Split RMS

    #new_zpoints = pol.polygon_plot(tpoints(100), new_coefs)






if __name__ == '__main__':
    main()

