""" Author Dahlia Dry
    Last Modified 1/9/2019
    A place to create comparative scatterplots for exoplanet-hosting and
    non-exoplanet-hosting stars
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from query import *

def convert_vars(vars):
    columns = []
    for var in vars:
        if var == "m_star":
            columns.append("mass")
        elif var == "r_star":
            columns.append("radius")
        elif var == "distance":
            columns.append('dist')
        elif var == "d_star":
            columns.append("dens")
        elif var == "n_planets":
            columns.append("nkoi")
        elif var == "eff_temp_star":
            columns.append("teff")
        elif var == "metallicity":
            columns.append("feh")
        elif var == "av_extinction":
            columns.append("av")
        else:
            return "whoops"
    return columns

def scatter(df, vars, xvar, yvar, xlabel, ylabel): #df is a dataframe obtained from QueryAll
    columns = convert_vars(vars)
    x0 = np.array(df[columns[0]])
    x1 = np.array(df[columns[1]])
    y = np.array(df['status'])
    new_x0 = []
    new_x1 = []
    new_y = []
    xmin = np.percentile(x0, 5)
    xmax = np.percentile(x0, 95)
    ymin = np.percentile(x1, 5)
    ymax = np.percentile(x1, 95)
    for i in range(len(x0)):
        if x0[i] > xmin and x0[i] < xmax and x1[i] > ymin and x1[i] < ymax:
            new_x0.append(x0[i])
            new_x1.append(x1[i])
            new_y.append(y[i])
    print(new_x0[:10])
    plt.scatter(new_x0, new_x1, c=new_y, s=1, cmap=plt.cm.Paired)
    plt.xlabel(xvar + " " + xlabel)
    plt.ylabel(yvar + " " + ylabel)
    plt.title(yvar + " vs " + xvar)
    plt.show()

vars = ['av_extinction', 'distance']
query = QueryAll(vars, filter = True, equalize = True)
df = query.getResults()
scatter(df, vars, xvar = "Stellar Av Extinction", yvar = "Distance", xlabel = "(mag)", ylabel = "(pc)")