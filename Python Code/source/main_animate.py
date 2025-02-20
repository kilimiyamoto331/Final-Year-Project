import numpy as np # for easy and fast number calculation
from math import tau # tau is constant number = 2*PI
import matplotlib.animation as animation # for compiling animation and exporting video 
import matplotlib.pyplot as plt # for plotting and creating figures
import data_io as io
import fourier as fr

#Once you run the code you will be given a prompt in the terminal asking you to specify a number to select a shape. Type a number and press enter to
#generate an animation of that shape being drawn out. Shape 18 was chosen for our poster. If you wish to save multiple animations scroll to the bottom
#of the code and change the name of the save file. 
 
## First find the coefficient that need to be animated and the zpoints array so that we can determine the dimensions of the animation.
N = 150
tpoints = np.arange(N)/N


#find coefficients
data = io.get_csv_data()
io.print_patterns(data)
coefs = io.get_coefs(data)
zpoints = fr.fourier_plot(tpoints, coefs)


#zpoints = io.get_boundary_points('star.png', N)
#coefs = fr.get_coefs_from_zpoints(zpoints, N)

## Finding the dimensions of the animation
# Find middle point  
order = int(coefs.size/2)
if ((coefs.size % 2) == 0):
    coefs = np.append(coefs, 0)


# Split the zpoints into x and y coordinates
x_list = np.real(zpoints)
y_list = np.imag(zpoints)

# Plot the x and y
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x_list, y_list)

# Find the dimensions of this plot and keep for later
xlim_data = plt.xlim() 
ylim_data = plt.ylim()


## Now to make the animation with epicycle

# this is to store the points of last circle of epicycle which draws the required figure
draw_x, draw_y = [], []

# make figure for animation
fig, ax = plt.subplots()

# different plots to make epicycle
# there are -order to order numbers of circles
circles = [ax.plot([], [], '#1f77b4')[0] for i in range(-order, order + (coefs.size % 2))]
# circle_lines are radius of each circles
#circle_lines = [ax.plot([], [], '#1f77b4')[0] for i in range(-order, order + (coefs.size % 2))]
# drawing is plot of final drawing
drawing, = ax.plot([], [], 'k-', linewidth=2)

# using the dimensions we found before, fix the size of figure so that the animation does not get cropped/trimmed
ax.set_xlim(xlim_data[0]-5, xlim_data[1]+5)
ax.set_ylim(ylim_data[0]-5, ylim_data[1]+5)

# hide axes if you want
#ax.set_axis_off()

# to have symmetric axes
ax.set_aspect('equal')

# Set up formatting for the video file
Writer = animation.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='me'), bitrate=1800)


# set number of frames, change this to speed up animation
frames = 150


# save the coefficients in order 0, 1, -1, 2, -2, ...
def sort_coef(coefs):
    new_coefs = []
    new_coefs.append(coefs[order])

    for i in range(1, order+1):
        new_coefs.extend([coefs[order+i],coefs[order-i]])
    return np.array(new_coefs)

# make frame at time t
# t goes from 0 to 2*PI for complete cycle
def make_frame(i, time, coefs):

    # get t from time
    t = time[i]

    # exponential term to be multiplied with coefficient 
    # this is responsible for making rotation of circle
    exp_term = np.array([np.exp(n*t*1j) for n in range(-order, order + (coefs.size % 2))])

    # sort the terms of fourier expression
    coefs = sort_coef(coefs*exp_term) 
    # coefs itself gives only direction and size of circle

    # split into x and y coordinates
    x_coefs = np.real(coefs)
    y_coefs = np.imag(coefs)

    # center the first circle at (0,0)
    center_x, center_y = x_coefs[0], y_coefs[0]
    x_coefs[0] = 0
    y_coefs[0] = 0

    # make all circles i.e epicycle
    for i, (x_coef, y_coef) in enumerate(zip(x_coefs, y_coefs)):
        # calculate radius of current circle
        r = np.linalg.norm([x_coef, y_coef]) 

        # draw circle with given radius at given center points of circle
        theta = np.linspace(0, tau, num=50) # theta goes from 0 to 2*PI to get all points of circle
        x, y = center_x + r * np.cos(theta), center_y + r * np.sin(theta) 
        circles[i].set_data(x, y)

        # draw a line to indicate the direction of circle
        x, y = [center_x, center_x + x_coef], [center_y, center_y + y_coef]
        #circle_lines[i].set_data(x,y)

        # calculate center for next circle
        center_x, center_y = center_x + x_coef, center_y + y_coef
    
    # center points now are points from last circle
    # these points are used as drawing points
    draw_x.append(center_x)
    draw_y.append(center_y)

    # draw the curve from last point
    drawing.set_data(draw_x, draw_y)





# time is from 0 to tau 
time = np.linspace(0, tau, num=frames)
# make animation
anim = animation.FuncAnimation(fig, make_frame, frames=frames, fargs=(time, coefs),interval=5)
# save animation to a mp4 file
anim.save('Circular_Animation.mp4', writer=writer)
