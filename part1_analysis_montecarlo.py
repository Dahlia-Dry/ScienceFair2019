import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os


class Monte_Carlo(object):
    """******Monte Carlo Data Analysis******
    Parameters
    ----------
    var = list of three right ascensions in degrees
    delta = list of three declinations in degrees
    sigmaA = corresponding list of uncertainties on each right ascension, obtained through LSPR
    sigmaD = corresponding list of uncertainties on each declination, obtained through LSPR
    N = number of simulations
    as of 7/20/2018, distributions look a bit sketchy
    """

    def __init__(self, alpha, sigmaA, delta, sigmaD, N):
        self.alpha = alpha
        self.delta = delta
        self.sigmaA = sigmaA
        self.sigmaD = sigmaD
        self.N = N

    def populate_alpha(self):
        """Generates N alphas,deltas using a random normal distribution."""
        alphas = []
        deltas = []
        for i in range(self.N):
            alphas.append(np.random.normal(self.alpha, self.sigmaA))
        return alphas

    def populate_delta(self):
        deltas = []
        for i in range(self.N):
            deltas.append(np.random.normal(self.delta, self.sigmaD))
        return deltas

    def remove_outliers(self, x):
        q1a = np.percentile(x, 25)
        q3a = np.percentile(x, 75)
        for i in x:
            if i < q1a or i > q3a:
                x.remove(i)
        return x

    def plot_population(self, kind):
        """plots the generated right ascension or declination values in a histogram.
            kind: string, = 'alpha' or 'delta', determines data and labels used."""
        if kind == 'alpha':
            x = self.populate_alpha()
            n, bins, patches = plt.hist(x, 70, normed=1, facecolor='blue')
            y = mlab.normpdf(bins, self.alpha, self.sigmaA)
            l = plt.plot(bins, y, 'r--', linewidth=1)
            plt.xlabel('Right Ascension')
            plt.ylabel('Probability')
            plt.show()
        if kind == 'delta':
            x = self.populate_delta()
            n, bins, patches = plt.hist(x, 70, normed=1, facecolor='blue')
            y = mlab.normpdf(bins, self.delta, self.sigmaD)
            l = plt.plot(bins, y, 'r--', linewidth=1)
            plt.xlabel('Declination')
            plt.ylabel('Probability')
            plt.show()

    def plot_distr(self, x, kind):
        """Plots the distribution of an orbital element.
            kind is a string determining the x label.
            x is a 1D list of generated orbital elements."""
        n, bins, patches = plt.hist(x, 70, normed=1, facecolor='darkturquoise')
        y = mlab.normpdf(bins, np.mean(x), np.std(x))
        l = plt.plot(bins, y, 'r--', linewidth=1)
        plt.xlabel(kind)

        title = 'Distribution of ' + kind + ' for ' + str(self.N) + ' Simulations'
        plt.title(title)
        plt.show()