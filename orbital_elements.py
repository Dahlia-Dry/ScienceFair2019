import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os

script_dir = os.path.dirname(__file__)
loadpath1 = 'data/planetdatamod.csv'
loadpath2 = 'data/stardatamod.csv'
planetdata = pd.read_csv(loadpath1, sep = ",")
stardata = pd.read_csv(loadpath2, sep = ",")

class OrbitalElements(object):
    def __init__(self, ):

