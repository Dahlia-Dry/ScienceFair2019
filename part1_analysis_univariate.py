""" Author Dahlia Dry
    Last Modified 1/9/2019
    Generates histograms and calculates distribution data
"""
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
       xvar: variable to query from database
       """
    def __init__(self, xvar):
        self.xvar = xvar

    def get_data(self):
        query = QueryAll([self.xvar])
        coords = query.getResults()
        return coords

    def make_histogram(self, bins, xlabel, units):
        coords = self.get_data()
        new_x = []
        q1 = np.percentile(coords,5)
        q3 = np.percentile(coords,95)
        for val in x:
            if val > q1 and val < q3:
                new_x.append(val)
        n, bins, patches = plt.hist(new_x, bins)
        plt.xlabel(xlabel+ "(" + units + ")" )
        plt.ylabel("frequency")
        plt.title("Distribution of " + xlabel + " in Kepler Data")
        plt.show()

    def get_mean(self):
        coords = self.get_data()
        return np.mean(coords)

    def get_sdev(self):
        coords = self.get_data()
        return np.std(coords)

def main():
    histograms = Part1_Univariate_Analysis('av_extinction')
    histograms.make_histogram(bins =30, xlabel = "Av Extinction", units= "mag")


main()