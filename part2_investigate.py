""" Author Dahlia Dry
    Last Modified 1/9/2019
    A dumping ground for hunches and testing of random bits
"""
from query import *
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np

query = QueryAll(['av_extinction', 'ra', 'dec'], filter = False, equalize = False)
df = query.getResults()
ramin = np.array(df['ra']).min()
ramax = np.array(df['ra']).max()
decmin = np.array(df['dec']).min()
decmax = np.array(df['dec']).max()
y = np.array(df['dec'])
z = np.array(df['av'])

print(ramin, ramax)
print(decmin, decmax)
fig = plt.figure()
ax = fig.gca(projection='3d')

# Make the grid
x, y, z = np.meshgrid(x,y,z)

ax.scatter(x,y,z)

plt.show()