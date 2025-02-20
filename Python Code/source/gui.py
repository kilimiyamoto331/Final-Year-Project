'''
@file: gui.py
@author: Anthony White and Kili Miyamoto
@date: 22/03/2023
@brief: Implements the GUI for viewing output shape and Fourier coefficients.
'''

# Import dependancies
import sys
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
from PyQt6 import QtWidgets as qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

convert_db = lambda x : 20*np.log10(x + 10**(-6))

class ShapePlot(FigureCanvasQTAgg):
    '''Constructor for creating a plot of the shape based on output of 
    the Fourier series calculation.

    args:
        width : int specifying figure width
        height : int specifying figure height
        zpoints1 : numpy array of z values to be plotted to draw shape 1
        zpoints2 : numpy array of z values to be plotted to draw shape 2
    
    '''

    def __init__(self, width, height, zpoints1, zpoints2):

        fig = Figure(figsize=(width, height), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.grid()
        self.ax.set_aspect('equal')
        self.ax.set(title = 'Shape', xlabel='Real', ylabel='Imaginary')
        self.ax.scatter(np.real(zpoints1), np.imag(zpoints1))
        if zpoints2.all():
            self.ax.scatter(np.real(zpoints2), np.imag(zpoints2))

        super(ShapePlot, self).__init__(fig)

class CoefPlot(FigureCanvasQTAgg):
    '''Constructor for creating a plot of the Fourier coefficients on the complex plane.

    args:
        width : int specifying figure width
        height : int specifying figure height
        coefs1 : numpy array of coefficients used to draw shape 1
        coefs2 : numpy array of coefficients used to draw shape 2
    
    '''

    def __init__(self, width, height, coefs1, npoints1, coefs2, npoints2):

        fig = Figure(figsize=(width, height), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.grid()
        self.ax.set_aspect('auto')
        self.ax.set(title = 'Fourier Descriptors', xlabel='Real', ylabel='Imaginary')

        self.ax.scatter(np.real(coefs1), np.imag(coefs1))
        np.vectorize(self.ax.text)(np.real(coefs1), np.imag(coefs1), npoints1, fontsize=11)
        print(coefs2.all())

        if np.any(coefs2):
            self.ax.scatter(np.real(coefs2), np.imag(coefs2))
            np.vectorize(self.ax.text)(np.real(coefs2), np.imag(coefs2), npoints2, fontsize=11)

        super(CoefPlot, self).__init__(fig)

class CoefStem(FigureCanvasQTAgg):
    '''Constructor for creating a stem plot of the Fourier Coefficients.

    args:
        width : int specifying figure width
        height : int specifying figure height
        coefs1 : numpy array of coefficients used to draw shape 1
        coefs2 : numpy array of coefficients used to draw shape 2
    
    '''
    
    def __init__(self, width, height, coefs1, npoints1, coefs2, npoints2, db, mag):

        fig = Figure(figsize=(width, height), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.grid()
        self.ax.set_aspect('auto')
        if mag:
            if db:
                self.ax.set(title = 'Magnitude of Fourier Descriptors (dB)', xlabel='n', ylabel='20*log|cn|')
            else:
                self.ax.set(title = 'Magnitude of Fourier Descriptors', xlabel='n', ylabel='|cn|')
        else:
            self.ax.set(title = 'Phase of Fourier Descriptors', xlabel='n', ylabel='arg(cn)')

        if np.any(coefs2): self.ax.stem(npoints2, coefs2, 'orange')
        self.ax.stem(npoints1, coefs1)

        super(CoefStem, self).__init__(fig)

class CoefHist(FigureCanvasQTAgg):

    def __init__(self, width, height, coefs1, npoints1, coefs2, npoints2):
        fig = Figure(figsize=(width, height), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.grid()
        self.ax.set_aspect('auto')
        self.ax.set(title = 'Phase of Fourier Descriptors (Histogram)', xlabel='arg(cn)')
        #if np.any(coefs2): self.ax.hist(npoints2, coefs2, 'orange')
        self.ax.hist(coefs1, 50)
        super(CoefHist, self).__init__(fig)

class MainWindow(qt.QMainWindow):
    '''Constructor for creating the PyQt window.

    args:
        zpoints1 : numpy array of z values to be plotted to draw shape 1
        coefs1 : numpy array of coefficients used to draw shape 1
        zpoints2 : numpy array of z values to be plotted to draw shape 2
        coefs2 : numpy array of coefficients used to draw shape 2
    
    '''

    def __init__(self, zpoints1, coefs1, npoints1, zpoints2, coefs2, npoints2, shift):
        super(MainWindow, self).__init__()

        self.setGeometry(0, 0, 1600, 1000)

        layout = qt.QVBoxLayout()
        layout_figs1 = qt.QHBoxLayout()
        layout_figs2 = qt.QHBoxLayout()

        # Plot for the shape
        fig_shape = ShapePlot(width=5, height=4, zpoints1=zpoints1, zpoints2=zpoints2)
        layout_figs1.addWidget(fig_shape)

        # Plot for Fourier coefficients on the complex plane
        fig_coefs = CoefPlot(width=5, height=4, coefs1=coefs1, npoints1=npoints1, coefs2=coefs2, npoints2=npoints2)
        layout_figs2.addWidget(fig_coefs)

        # Plot for the magnitudes of Fourier coefficeints
        fig_coefs_mag = CoefStem(width=5, height=4, coefs1=np.abs(coefs1), npoints1=npoints1, coefs2=np.abs(coefs2), npoints2=npoints2, db=0, mag=1)
        layout_figs1.addWidget(fig_coefs_mag)

        # Plot for the magnitudes of Fourier coefficeints (dB)
        fig_coefs_mag_db = CoefStem(width=5, height=4, coefs1=convert_db(np.abs(coefs1)), npoints1=npoints1, coefs2=convert_db(np.abs(coefs2)), npoints2=npoints2, db=1, mag=1)
        layout_figs2.addWidget(fig_coefs_mag_db)

        # Set very small FDs to zero, to avoid random phase values
        coefs1[np.abs(coefs1) < 10**(-1)] = 0

        # Plot for the phase of the Fourier coefficients
        fig_coefs_phase = CoefStem(width=5, height=4, coefs1=np.angle(coefs1), npoints1=npoints1, coefs2=np.angle(coefs2), npoints2=npoints2, db=0, mag=0)
        layout_figs1.addWidget(fig_coefs_phase)

        # Plot for the phase of the Fourier coefficients (hist)
        fig_coefs_phase_hist = CoefHist(width=5, height=4, coefs1=np.angle(coefs1), npoints1=npoints1, coefs2=np.angle(coefs2), npoints2=npoints2)
        layout_figs2.addWidget(fig_coefs_phase_hist)

        layout.addLayout(layout_figs1)
        layout.addLayout(layout_figs2)

        widget = qt.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()
            
def create_window(zpoints1, coefs1, zpoints2=np.array([]), coefs2=np.array([])):
    '''Function to generate a GUI window to view plots of the shape(s) and 
    Fourier coeffeicients.

    args:
        zpoints1 : numpy array of z values to be plotted to draw shape 1
        coefs1 : numpy array of coefficients used to draw shape 1
        zpoints2 : (optional) numpy array of z values to be plotted to draw shape 2
        coefs2 : (optional) numpy array of coefficients used to draw shape 2
    
    '''

    # Set to one to centre coefficients around zero
    shift = 0

    # Determine coefs array size
    nsize1 = len(coefs1)
    npoints1 = np.linspace(0, nsize1-1, nsize1, dtype=int) - shift*int(nsize1/2)
    nsize2 = len(coefs2)
    npoints2 = np.linspace(0, nsize2-1, nsize2, dtype=int) - shift*int(nsize2/2)

    # Generate output window
    app = qt.QApplication(sys.argv)
    window = MainWindow(zpoints1, coefs1, npoints1, zpoints2, coefs2, npoints2, shift)
    app.exec()