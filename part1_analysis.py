import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os


class Part1_Univariate_Analysis(object):
    """*****UNIVARIATE DATA ANALYSIS*****
       Operations: Histograms
       Parameters
       ----------
       xvar: pandas series of data from one column of star or planet databanks
       """
    def __init__(self, xvar):
        self.xvar = xvar

    def make_histogram(self, binsize, xlabel, units):
        x = self.xvar.values
        n, bins, patches = plt.hist(x, binsize)
        plt.xlabel(xlabel + "(" + units + ")")
        plt.ylabel("frequency of " + xlabel)
        plt.title("Distribution of " + xlabel + " in Kepler Data")
        plt.show()


