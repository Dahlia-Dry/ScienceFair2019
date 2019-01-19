"""
Author Dahlia Dry
Last Modified 1/9/2019
This program is the flexible feature space SVM software used for a variety of applications
in the rest of this project.
"""

import numpy as np
import pandas as pd
from query import *
from sklearn import svm as svm
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.colors import ListedColormap
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

    def optimize_params(self):
        data = self.make_query()
        X,y = self.format_data(data, shuffle = False)
        kernel = ['rbf','poly','sigmoid']
        best_kern = 'rbf'
        max_score = 0
        for kern in kernel:
            model = svm.SVC(kernel= kern)
            model.fit(X,y)
            score = model.score(X,y)
            if score > max_score:
                max_score = score
                best_kern = kern
        return [best_kern]


    def get_probfloat(self, input): #outputs the probability of a given input set with same dimensions as vars having exoplanets
        data = self.make_query()
        X,y = self.format_data(data, shuffle = False)
        params = self.optimize_params()
        model = svm.SVC(kernel = params[0])
        model.fit(X,y)
        return model.predict_proba(input)

    def plot_feature_subset(self):
        data= self.make_query()
        X,y = self.format_data(data, shuffle = False)
        params = self.optimize_params()
        model = svm.SVC(kernel = params[0])
        model.fit(X,y)
        h = 0.2
        x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
        y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))

        fig = plt.figure()
        ax = fig.add_subplot(111)
        cm = plt.cm.RdBu
        cm_bright = ListedColormap(['#FF0000', '#0000FF'])
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap=cm_bright,
                   edgecolors='k')
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())
        Z = model.decision_function(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        ax.contourf(xx, yy, Z, cmap=cm, alpha=.8)
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap=cm_bright,
                   edgecolors='k')
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_xlabel("Stellar Density (g/cm^3)")
        ax.set_ylabel("Stellar Effective Temperature (K)")
        plt.tight_layout()
        plt.show()