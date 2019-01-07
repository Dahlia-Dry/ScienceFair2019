from query import *
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np

query = QueryAll(['av_extinction', 'ra', 'dec'], filter = True, equalize = True)
df = query.getResults()
x = np.array(df['ra'])
y = np.array(df['dec'])
z = 0
u= 0
v = 0
w = np.array(df['av'])

fig = plt.figure()
ax = fig.gca(projection='3d')

# Make the grid
x, y, z = np.meshgrid(x,y,z)

ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)

plt.show()