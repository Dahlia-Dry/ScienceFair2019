""" Author Dahlia Dry
    Last Modified 1/9/2019
    Performs qualitative multivariate analysis of Kepler data through scatterplots
    and surface triangulation diagrams
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from query import *
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


class Part1_Multivariate_Analysis(object):
    """"*****MULTIVARIATE DATA ANALYSIS*****

       varlist: list of variables to query from Kepler database
       
       """
    def __init__(self, varslist):
        self.varslist = varslist

    def gen_df(self):
        query = QueryAll(self.varslist, filter=True, equalize=True)
        db = query.getResults()
        return db

    def convert_vars(self):
        columns = []
        for var in self.varslist:
            if var == "ra":
                columns.append("ra")
            elif var == "dec":
                columns.append("dec")
            elif var == 'distance':
                columns.append("dist")
            elif var == "m_star":
                columns.append("mass")
            elif var == "r_star":
                columns.append("radius")
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

    def scatter(self, xlabel, ylabel, zlabel):
        db = self.gen_df()
        status = db['status']
        columns = self.convert_vars()
        x = db[columns[0]]
        y = db[columns[1]]
        z = db[columns[2]]
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        new_x = []
        new_y = []
        new_z = []
        new_status = []
        x1 = np.percentile(x, 10) #remove outliers
        x3 = np.percentile(x, 90)
        y1 = np.percentile(y, 10)
        y3 = np.percentile(y, 90)
        z1 = np.percentile(z, 10)
        z3 = np.percentile(z, 90)
        for i in range(len(x)):
            if x[i] > x1 and x[i] < x3 and y[i] > y1 and y[i] < y3 and z[i] > z1 and z[i] < z3:
                new_x.append(x[i])
                new_y.append(y[i])
                new_z.append(z[i])
                new_status.append(status[i])
        new_x = np.array(new_x)
        new_y = np.array(new_y)
        new_z = np.array(new_z)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        ax.scatter(new_x, new_y, new_z, c=new_status, cmap=plt.cm.Paired)
        plt.show()

    def trisurf(self, xlabel, ylabel, zlabel, cmap): #cmap viridis or magma
        db = self.gen_df()
        status = db['status']
        columns = self.convert_vars()
        x = db[columns[0]]
        y = db[columns[1]]
        z = db[columns[2]]
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        new_x = []
        new_y = []
        new_z = []
        new_status = []
        x1 = np.percentile(x, 10) #remove outliers
        x3 = np.percentile(x, 90)
        y1 = np.percentile(y, 10)
        y3 = np.percentile(y, 90)
        z1 = np.percentile(z, 10)
        z3 = np.percentile(z, 90)
        for i in range(len(x)):
            if x[i] > x1 and x[i] < x3 and y[i] > y1 and y[i] < y3 and z[i] > z1 and z[i] < z3:
                new_x.append(x[i])
                new_y.append(y[i])
                new_z.append(z[i])
                new_status.append(status[i])
        new_x = np.array(new_x)
        new_y = np.array(new_y)
        new_z = np.array(new_z)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)
        ax.plot_trisurf(new_x,new_y,new_z, cmap = cmap)
        plt.show()



def main():
    vars = ['av_extinction', 'distance','d_star']
    plot3d = Part1_Multivariate_Analysis(vars)
    plot3d.trisurf("Av Extinction",  "Distance", "Stellar Density", cmap = 'viridis')


main()

