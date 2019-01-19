""" Author Dahlia Dry
    Last Modified 1/9/2019
    Performs bivariate analysis of Kepler data through scatterplots,
    regression analysis, gaussian kernel density estimation
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from scipy import stats
from query import *


class Part1_Bivariate_Analysis(object):
    """*****BIVARIATE DATA ANALYSIS*****
       Operations: optimized fit regression, scatterplots,
       Parameters
       ----------
       coords: list of (x,y) tuples corresponding to two variables queried from the Kepler database
       """
    def __init__(self, coords):
        self.coords = coords

    def optimized_regression(self):
        deg = [1,2,3,4,5]
        resids = []
        x = [self.coords[i][0] for i in range(len(self.coords))]
        y = np.array([self.coords[i][1] for i in range(len(self.coords))])
        yhat = []
        coefs = []
        yval = 0
        power = 0
        for d in deg:
            coefs = np.polyfit(x,y,d)
            for val in x:
                yval = 0
                for c in range(len(coefs)):
                    power = len(coefs) - c
                    yval += coefs[c] * (val ** power)
                yhat.append(yval)
            yhat = np.array(yhat)
            resids.append([y[i] - yhat[i] for i in range(len(y))])
            yhat = []
        sums = []
        for r in resids:
            sum = 0
            for val in resids[r]:
                sum += math.abs(val)
            sums.append(sum)
        minsum = 1000000
        index = 0
        for s in range(len(sums)):
            if sums[s] < minsum:
                index = s

        return np.polyfit(x,y,deg[index]) #returns coefficients of optimized regression line


    def get_rvals(self):
        x = [self.coords[i][0] for i in range(len(self.coords))]
        y = [self.coords[i][1] for i in range(len(self.coords))]
        r = np.corrcoef(x,y)
        return r, r**2

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

    def gaussian_kde(self,xlabel,xunits,ylabel,yunits):
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
        new_x = np.array(new_x)
        new_y = np.array(new_y)
        xmin = new_x.min()
        xmax = new_x.max()
        ymin = new_y.min()
        ymax = new_y.max()
        xprime,yprime = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([xprime.ravel(), yprime.ravel()])
        values = np.vstack([new_x,new_y])
        kernel = stats.gaussian_kde(values)
        z = np.reshape(kernel(positions).T, xprime.shape)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(np.rot90(z), cmap = plt.cm.gist_earth_r, extent = [xmin,xmax, ymin, ymax])
        ax.plot(new_x,new_y,'k.', markersize = 1)
        ax.set_xlim([xmin,xmax])
        ax.set_ylim([ymin,ymax])
        plt.xlabel(xlabel + "(" + xunits + ")")
        plt.ylabel(ylabel + "(" + yunits + ")")
        plt.title("Gaussian Kernel Density Estimation for " + ylabel + " vs " + xlabel)
        plt.show()



def main():
    query = QueryCandidates(["d_planet", "r_star"])
    coordinates = query.getResults()
    scatterplot = Part1_Bivariate_Analysis(coordinates)
    scatterplot.gaussian_kde("Planet Density", "jupiter radii", "Stellar Radius", "solar radii")

main()