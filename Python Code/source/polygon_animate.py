import numpy as np # for easy and fast number calculation
import matplotlib.animation as animation # for compiling animation and exporting video 
import matplotlib.pyplot as plt # for plotting and creating figures
import data_io as io
from math import tau # tau is constant number = 2*PI
import polygon as pol

poly_func = lambda k, N, t : np.exp(1j*2*np.pi*k/N*np.floor(N*t))*(1+(np.exp(1j*2*np.pi*k/N)-1)*(N*t-np.floor(N*t)))


def make_animation(coefs, name):
    ## First find the coefficient that need to be animated.

    # Find the size of the coefficients array, this value will be used in many steps
    N = coefs.size

    # set number of frames, change this to speed up animation
    frames = 250
    time = np.arange(0, frames) / frames

    ## Find the zpoints array so that we can determine the dimensions of the animation.
    # Create a copy of the coefficients so we dont alter the original and make the first value so that plot is centered at (0,0)
    coefs[0] = 0
    zpoints = pol.polygon_plot(time, coefs)

    # split into x and y coefficients
    x_list = np.real(zpoints)
    y_list = np.imag(zpoints)

    # Plot the x and y
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x_list, y_list)

    # Find the dimensions of this plot and keep for later
    xlim_data = plt.xlim() 
    ylim_data = plt.ylim()


    ## Now to make the animation 

    # this is to store the points of last circle of epicycle which draws the required figure
    draw_x, draw_y = [], []

    # make figure for animation
    fig, ax = plt.subplots()

    # different plots to make epicycle
    # there are -order to order numbers of sub polygons
    sub_polygon_plot = [ax.plot([], [], '#1f77b4')[0] for i in range(0, frames)]
    # points of where the centers are
    center_points = [ax.plot([], [], '#1f77b4')[0] for i in range(0, frames)]
    # drawing is plot of final drawing
    drawing, = ax.plot([], [], 'k-')

    # using the dimensions we found before, fix the size of figure so that the animation does not get cropped/trimmed
    ax.set_xlim(xlim_data[0]*1.35, xlim_data[1]*1.35)
    ax.set_ylim(ylim_data[0]*1.35, ylim_data[1]*1.35)

    # to have symmetric axes
    ax.set_aspect('equal')

    # Set up formatting for the video file
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=30, metadata=dict(artist='me'), bitrate=1800)




    # sort the polygons in order of largest to smallest for a better looking animation
    def sort_poly(sub_poly):
        #set up the necessary variables
        sorted_poly = np.zeros((N-1, frames), dtype=np.complex_)
        max_value = 0
        max_index = 0

        #easiest way to find the biggest is to find the max value in each sub_poly array and compare
        for i in range(0, N-1): #loop through each sub_poly 
            for k in range (0, N-1): #loop through each sub_poly again however this time look for max
                if (max_value < max(sub_poly[k])):  #typical max finding if statement
                    max_value = max(sub_poly[k])
                    max_index = k                   #store index of the sub_poly with max value

            sorted_poly[i] = sub_poly[max_index] #copy the biggest sub_poly in the new sorted 2d matrix
            sub_poly[max_index] = 0              #replace the biggest sub_poly with zero so it wont be found again
            max_value = 0                        #reset max value
            


        return sorted_poly


    def make_frame(i, coef, sub_poly):

        #make a copy since we need to change values in sub_poly each time but still want to 
        #keep the original array in tact 
        added_sub_poly = sub_poly.copy()    

        #find the next point in each sub_polygon, these will be the center points for the sub_polygon
        points = np.zeros(N-1, dtype=np.complex_)
        points[0] = sub_poly[0][i]

        #accumulate points cause the sub_polygon add on to each other
        for k in range(1, N-1):  
            points[k] = points[k-1] + sub_poly[k][i]

        
        # split into x and y coefficients
        x_coefs = np.real(points)
        y_coefs = np.imag(points)

        theta = np.linspace(0, tau, num=50) # theta should go from 0 to 2*PI to get all points of circle

        #loop to draw the sub_polygons
        for q, (x_coef, y_coef) in enumerate(zip(x_coefs, y_coefs)):

            #draw the sub_polygon
            x = np.real(added_sub_poly[q])
            y = np.imag(added_sub_poly[q])
            sub_polygon_plot[q].set_data(x, y)

            if (q+1 == N-1):
                break
            
            #create a circle since an actual point is too small to see
            x, y = x_coef + 0.5 * np.cos(theta), y_coef + 0.5 * np.sin(theta)

            center_points[q+1].set_data(x, y)
            #add the center value to every element in the next sub_polygon array to shift it to its new position
            added_sub_poly[q+1] = added_sub_poly[q+1] + x_coef + 1j*y_coef
            
        
        # the last center points is the final z point so use it to draw the actual shape
        draw_x.append(x_coefs[N-2])
        draw_y.append(y_coefs[N-2])

        # draw the curve
        drawing.set_data(draw_x, draw_y)






    sub_poly = np.zeros((N-1, frames), dtype=np.complex_)

    # find the sub_poly using the equation but ignore the first one since its not a sub_poly but locational information
    for k in range(0, N-1):  
        sub_poly[k] = 1/N*coefs[k+1]*poly_func(k+1, N, time)




    #sort the sub_polygons from largest to smallest
    sub_poly = sort_poly(sub_poly)

    # make animation
    anim = animation.FuncAnimation(fig, make_frame, frames=frames, fargs=(coefs, sub_poly),interval=5)
    anim.save(name, writer=writer)
