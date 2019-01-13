import numpy as np
import pandas as pd
from query import *
from sklearn import svm as svm
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')


class SVM(object):
    def __init__(self, vars):
        self.vars = vars

    def convert_vars(self):
        columns = []
        for var in self.vars:
            print(var)
            if var == "m_star":
                columns.append("mass")
            elif var == "r_star":
                columns.append("radius")
            elif var == 'distance':
                columns.append("dist")
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

    def make_query(self): #use query class to get a dataframe
        print("called it")
        query = QueryAll(self.vars, filter = True, equalize = True)
        data = query.getResults()
        print(len(data))
        return data

    def format_data(self, df, shuffle): #use dataframe to make x, y
        if shuffle:
            df = df.sample(frac=1).reset_index(drop=True)
        x = []
        y = np.array(df['status'])
        print(y[0])
        coord = []
        columns = self.convert_vars()
        for i in range(len(df['status'])):
            for col in columns:
                coord.append(float(df[col].iloc[i]))
            x.append(coord)
            coord = []
        print(x[0])
        x = np.array(x)
        return x,y

    def create(self): #synthesize it
        data= self.make_query()
        x,y = self.format_data(data, shuffle = False)
        print(x,y)
        model = svm.SVC()
        model.fit(x,y)
        print('score:',model.score(x,y))

        print(model.predict([[.315,-.08],[.289,.07], [.428,.16], [.388,.16]]))
        plt.scatter(x[:,0], x[:,1], c= y, s=1, cmap = plt.cm.Paired)
        plt.show()
        """ax = plt.gca()
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        xx = np.linspace(xlim[0], xlim[1], 30)
        yy = np.linspace(ylim[0], ylim[1], 30)
        YY,XX = np.meshgrid(yy,xx)
        xy = np.vstack([XX.ravel(), YY.ravel()]).T
        Z = model.decision_function(xy).reshape(XX.shape)
        ax.contour(XX,YY,Z,colors= 'k', levels = [-1,0,1], alpha = 0.5,
                   linestyles = ['--', '-', '--'])
        ax.scatter(model.support_vectors_[:,0], model.support_vectors_[:,1], s = 2,
                   linewidth = 1, facecolors = 'none', edgecolors = 'k')
        plt.show()
        x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
        y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
        h = 0.2
        xprime, yprime = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        plt.subplot(1, 1, 1)
        Z = model.predict(np.c_[xprime.ravel(), yprime.ravel()])
        Z = Z.reshape(xprime.shape)
        plt.contourf(xprime, yprime, Z, cmap=plt.cm.Paired, alpha=0.8)
        plt.scatter(x[:, 0], x[:, 1], c=y, cmap=plt.cm.Paired)
        plt.xlabel('AV Extinction')
        plt.ylabel('Metallicity')
        plt.xlim(xprime.min(), xprime.max())
        plt.title('SVC with Linear kernel')
        plt.show()"""

e = SVM(['d_star', 'eff_temp_star'])
e.create()

