import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os


class Part1_Bivariate_Analysis(object):
    """*****BIVARIATE DATA ANALYSIS*****
       Operations: optimized fit regression, scatterplots,
       Parameters
       ----------
       xvar: pandas series of data from one column of star or planet databanks
       yvar: pandas series of data from one column of star or planet databanks
       """
    def __init__(self, xvar, yvar):
        self.xvar = xvar
        self.yvar = yvar

    def get_correlation_coefficient(self):
        """Obtain the r and r^2 values for the correlation between the given variables.
           Optimized by finding the best r value from a variety of fits."""
        ''