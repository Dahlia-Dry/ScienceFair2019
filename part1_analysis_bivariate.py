import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from query import *


class Part1_Bivariate_Analysis(object):
    """*****BIVARIATE DATA ANALYSIS*****
       Operations: optimized fit regression, scatterplots,
       Parameters
       ----------
       xvar: pandas series of data from one column of star or planet databanks
       yvar: pandas series of data from one column of star or planet databanks
       """
    def __init__(self, coords):
        self.coords = coords

    def get_correlation_coefficient(self):
        """Obtain the r and r^2 values for the correlation between the given variables.
           Optimized by finding the best r value from a variety of fits."""
        print("wip")

    def scatterplot(self, xlabel, xunits, ylabel, yunits):
        x = [self.coords[i][0] for i in range(len(self.coords))]
        y = [self.coords[i][1] for i in range(len(self.coords))]
        new_x = []
        new_y = []
        x1 = np.percentile(x, 10)
        x3 = np.percentile(x, 90)
        y1 = np.percentile(y, 10)
        y3 = np.percentile(y, 90)
        for i in range(len(x)):
            if x[i] > x1 and x[i] < x3 and y[i] > y1 and y[i] < y3:
                new_x.append(x[i])
                new_y.append(y[i])

        plt.scatter(new_x,new_y, color = "red", s = .75)
        plt.xlabel(xlabel + "(" + xunits + ")")
        plt.ylabel(ylabel + "(" + yunits + ")")
        plt.title(ylabel + " vs " + xlabel)
        plt.show()


query = QueryCandidates(["r_star", "irmag"])
coordinates = query.getResults()
scatterplot = Part1_Bivariate_Analysis(coordinates)
scatterplot.scatterplot("Stellar Radius", "solar radii", "Near-Infrared Magnitude", "")