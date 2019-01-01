import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from query import *

class Part1_Univariate_Analysis(object):
    """*****UNIVARIATE DATA ANALYSIS*****
       Operations: Histograms
       Parameters
       ----------
       xvar: list of data from one column of star or planet databanks
       """
    def __init__(self, xvar):
        self.xvar = xvar

    def make_histogram(self, bins, xlabel, units):
        x = self.xvar
        new_x = []
        q1 = np.percentile(x,5)
        q3 = np.percentile(x,95)
        for val in x:
            if val > q1 and val < q3:
                new_x.append(val)
        n, bins, patches = plt.hist(new_x, bins)
        plt.xlabel(xlabel+ "(" + units + ")" )
        plt.ylabel("frequency")
        plt.title("Distribution of " + xlabel + " in Kepler Data")
        plt.show()


query = Query(["semi-major axis"])
coordinates = query.getResults()
histograms = Part1_Univariate_Analysis([coordinates[i][0] for i in range(len(coordinates))])
histograms.make_histogram(bins =60, xlabel = "Semi-Major Axis", units= "AU")
