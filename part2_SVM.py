import numpy as np
import pandas as pd
from query import *
from sklearn import svm as svm
import matplotlib.pyplot as plt


class SVM(object):
    def __init__(self, vars):
        self.vars = vars

    def convert_vars(self):
        columns = []
        for var in self.vars:
            if var == "m_star":
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

    def make_query(self): #use query class to get a dataframe
        query = QueryAll(self.vars)
        data = query.getResults()
        return data

    def format_data(self, df): #use dataframe to make x, y
        x = []
        y = df['status'].tolist()
        coord = [0,0]
        columns = self.convert_vars()
        for i in range(len(df['status'])):
            coord[0] = df[columns[0]].iloc[i]
            coord[1] = df[columns[1]].iloc[i]
            x.append(coord)
            coord = [0,0]
        return x,y

    def create(self): #synthesize it
        data= self.make_query()
        x,y = self.format_data(data)
        model = svm.SVC(gamma = 'scale')
        return model

e = SVM(['av_extinction', 'metallicity'])
model = e.create()
model.fit(gamma = 'scale')
print(model.score(x,y))
