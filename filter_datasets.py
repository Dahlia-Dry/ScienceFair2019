import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os

script_dir = os.path.dirname(__file__)
loadpath1 = 'data/exomultpars.csv'
loadpath2 = 'data/keplerstellar.csv'
loadpath3 = 'data/cumulative.csv'
planetdata = pd.read_csv(loadpath1, sep = ",")
stardata = pd.read_csv(loadpath2, sep = ",")
koimaster = pd.read_csv(loadpath3, sep = ",")


#initial filter for stardata- check for and eliminate empty mass,radius,density fields
for i in range(len(stardata["kepid"])):
    if str(stardata["mass"].iloc[i]) == "nan" or str(stardata["dens"].iloc[i]) == "nan" or str(stardata["radius"].iloc[i]) == "nan":
        stardata.drop([i])
        print("1 " + str(i))
    else:
        print("1 keep " + str(i))

stardata.reset_index(drop=True)
print("done1")

#initial filter for planetdata- check for duplicate planet observations (there's a lot)
for i in range(len(planetdata["mpl_hostname"])):
    planet = str(planetdata["mpl_hostname"].iloc[i]) + str(planetdata["mpl_letter"].iloc[i])
    for j in range(len(planetdata["mpl_hostname"])):
        if j != i and planet == str(planetdata["mpl_hostname"].iloc[j]) + str(planetdata["mpl_letter"].iloc[j]):
            planetdata.drop(j)
            print("2 " + str(i) + " " + str(j))
        else:
            print("2 keep " + str(i) + " " + str(j))

planetdata.reset_index(drop=True)
print("done2")

#match kepIDs and id numbers to KOI catalog, use KOI catalog as master
starmatch = False
planetmatch = False
for i in range(len(stardata["kepid"])):
    for j in range(len(koimaster["kepid"])):
        if str(koimaster["kepid"].iloc[j]) == str(stardata["kepid"].iloc[i]):
            starmatch = True
            break
    if starmatch == False:
        stardata.drop([i])
        print("3 " + str(i) + " " + str(j))
    else:
        print("3 keep " + str(i))
    starmatch = False

stardata.reset_index(drop=True)
print("done3")

for k in range(len(planetdata["mpl_hostname"])):
    if str(planetdata["mpl_hostname"].iloc[k])[:3] == "KOI": #convert to koimaster syntax
        length = len(str(planetdata["mpl_hostname"].iloc[k])[5:])
        bufferstring = "K"
        bufferstring = [bufferstring + "0" for i in range(len(5-length))]
        bufferstring = bufferstring + str(planetdata["mpl_hostname"].iloc[k])[5:]
        print(bufferstring)
    for l in range(len(koimaster["kepid"])):
        if "KIC " + str(koimaster["kepid"].iloc[l]) == str(planetdata["mpl_hostname"].iloc[k]):
            planetmatch = True
            break
        elif bufferstring == str(koimaster["kepoi_name"].iloc[l]):
            planetmatch = True
            break
        elif str(planetdata["mpl_hostname"].iloc[k]) + str(planetdata["mpl_letter"].iloc[k]) == str(planetdata["kepler_name"].iloc[l]):
            planetmatch = True
            break
    if planetmatch == False:
        planetdata.drop(k)
        print("4 " + str(k) + " " + str(l))
    else:
        print("4 keep " + str(k) + " " + str(l))
    planetmatch = False
planetdata.reset_index(drop=True)
print("done4")


savepath1 = 'data/stardatamod.csv'
savepath2 = 'data/planetdatamod.csv'
stardata.to_csv(savepath1)
planetdata.to_csv(savepath2)

