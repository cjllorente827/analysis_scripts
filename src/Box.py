"""Simple class for defining a box with a center and side length
offers convenience methods for retrieving lower left and upper right points
basically I'm just tired of doing the same geometry over and over

The box spec file should be a csv with the x, y, z of the center followed by the length
i.e.
0.5, 0.5, 0.5, 1
"""

import numpy as np

class Box:

    def __init__(self, filename=None):

        if filename == None:
            self.center = np.array([0.5,0.5,0.5])
            self.length = 1.
        else:
            *self.center, self.length = np.genfromtxt(filename, delimiter=',', unpack=True)


    def __str__(self):
        return f"A box located at ({self.x},{self.y},{self.z}) with side length {self.length}"
    
    def lowerLeft(self):

        return self.center - self.length/2
    
    def upperRight(self):

        return self.center + self.length/2
