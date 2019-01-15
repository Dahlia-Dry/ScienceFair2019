import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os
from query import *
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


"""class Part1_Multivariate_Analysis(object):
    *****MULTIVARIATE DATA ANALYSIS*****
       Operations: Monte Carlo Variability Simulation, Histograms,
       Parameters
       ----------
       varlist: list of pandas series taken from star or planet databases
       
       """

vars = ['av_extinction', 'distance','d_star']
query = QueryAll(vars, filter = True, equalize=  True)
db = query.getResults()
status = db['status']
x = db['av']
y = db['dist']
z = db['dens']
"""x = [db[i][0] for i in range(len(db))]
y = [db[i][1] for i in range(len(db))]
z = [db[i][2] for i in range(len(db))]"""
"""for i in range(len(db['mass'])):
    if db['status'].iloc[i] == 1:
        x.append(db['mass'].iloc[i])
        y.append(db['radius'].iloc[i])
        z.append(db['dens'].iloc[i])"""
x = np.array(x)
y = np.array(y)
z = np.array(z)
new_x = []
new_y = []
new_z = []
new_status = []
x1 = np.percentile(x, 10)
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
ax.set_xlabel("Av Extinction (mag)")
ax.set_ylabel("Distance (pc)")
ax.set_zlabel("Stellar Effective Temperature (K)")
ax.scatter(new_x,new_y,new_z, c = new_status, cmap=plt.cm.Paired)
#ax.plot_trisurf(new_x,new_y,new_z, cmap = 'viridis')
plt.show()