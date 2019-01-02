import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os

script_dir = os.path.dirname(__file__)
loadpath1 = 'data/planetdatamod2.csv'
loadpath2 = 'data/stardatamod3.csv'
loadpath3 = 'data/cumulative.csv'
loadpath4= 'data/compositepars.csv'
planetdata = pd.read_csv(loadpath1, sep = ",")
planetdata = planetdata.reset_index(drop=True)
stardata = pd.read_csv(loadpath2, sep = ",")
koimaster = pd.read_csv(loadpath3, sep = ",")
composite = pd.read_csv(loadpath4, sep = ",")

print(len(planetdata["mpl_hostname"]))
print(len(stardata["kepid"]))

def starfilter1(stardata):#initial filter for stardata- check for and eliminate empty mass,radius,density fields
    length = len(stardata["kepid"])
    badindices = []
    for i in range(length):
        if str(stardata["mass"].iloc[i]) == "nan" or str(stardata["dens"].iloc[i]) == "nan" or str(stardata["radius"].iloc[i]) == "nan":
            badindices.append(i)
            print("1 " + str(i))
        else:
            print("1 keep " + str(i))
    stardata = stardata.drop(badindices)
    stardata = stardata.reset_index(drop=True)

    print("done1")
    savepath11 = 'data/stardatamod1.csv'
    savepath21 = 'data/planetdatamod1.csv'
    stardata.to_csv(savepath11)
    planetdata.to_csv(savepath21)
    print(len(stardata["kepid"]))

def planetfilter2(planetdata):#initial filter for planetdata- check for duplicate planet observations (there's a lot)
    print(len(planetdata["mpl_hostname"]))
    planet = ""
    badindices = []
    i = 0
    while i < len(planetdata["mpl_hostname"]):
        planet = str(planetdata["mpl_hostname"].iloc[i]) + str(planetdata["mpl_letter"].iloc[i])
        for j in range(len(planetdata["mpl_hostname"])):
            if planet == str(planetdata["mpl_hostname"].iloc[j]) + str(planetdata["mpl_letter"].iloc[j]):
                print("yes dood")
                if j != i and j>i:
                    print(planet)
                    print(str(planetdata["mpl_hostname"].iloc[j]) + str(planetdata["mpl_letter"].iloc[j]))
                    badindices.append(j)
                    print(badindices)
                    print("2 " + str(i) + " " + str(j))
                    i = i + 1
        i = i + 1

    planetdata = planetdata.drop(badindices)
    planetdata.reset_index(drop=True)
    print("done2")
    print(len(planetdata["mpl_hostname"]))
    savepath12 = 'data/stardatamod2.csv'
    savepath22 = 'data/planetdatamod2.csv'
    stardata.to_csv(savepath12)
    planetdata.to_csv(savepath22)

def starfilter3(stardata):#match kepIDs and id numbers to KOI catalog, use KOI catalog as master
    print(len(stardata["kepid"]))
    badindices = []
    starmatch = False
    planetmatch = False
    for i in range(len(stardata["kepid"])):
        for j in range(len(koimaster["kepid"])):
            if str(koimaster["kepid"].iloc[j]) == str(stardata["kepid"].iloc[i]):
                starmatch = True
                break
        if starmatch == False:
            badindices.append(i)
            print("3 " + str(i) + " " + str(j))
        else:
            print("3 keep " + str(i))
        starmatch = False
    stardata = stardata.drop(badindices)
    stardata = stardata.reset_index(drop=True)
    print("done3")
    savepath13 = 'data/stardatamod3.csv'
    savepath23 = 'data/planetdatamod3.csv'
    stardata.to_csv(savepath13)
    planetdata.to_csv(savepath23)

def planetfilter4(planetdata):
    bufferstring = ""
    planetmatch = False
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

def matchfilter(stardata, koimaster, planetdata):
    bufferstring = ""
    starmatch = False
    good_indices = []
    selected_indices = []
    bad_indices = []
    zerostring = ""
    for k in range(len(planetdata["mpl_hostname"])):
        if str(planetdata["mpl_hostname"].iloc[k])[:3] == "KOI":  # convert to koimaster syntax
            length = len(str(planetdata["mpl_hostname"].iloc[k])[4:])
            bufferstring = "K"
            for i in range(5-length):
                zerostring = zerostring + "0"
            zerostring = str(zerostring)
            bufferstring = bufferstring + zerostring
            bufferstring = bufferstring + str(planetdata["mpl_hostname"].iloc[k])[4:]
            print(bufferstring)
        for l in range(len(koimaster["kepid"])):
            if "KIC " + str(koimaster["kepid"].iloc[l]) == str(planetdata["mpl_hostname"].iloc[k]):
                selected_indices.append(l)
                print("selected1")
                break
            elif bufferstring == str(koimaster["kepoi_name"].iloc[l])[:6]:
                selected_indices.append(l)
                print("selected2")
                break
            elif str(planetdata["mpl_hostname"].iloc[k]) + " " + str(planetdata["mpl_letter"].iloc[k]) == str(koimaster["kepler_name"].iloc[l]):
                selected_indices.append(l)
                print("selected3")
                break
        bufferstring = ""
        zerostring = ""
        print(k, planetdata["mpl_hostname"].iloc[k])
    print(selected_indices)
    print(len(selected_indices)) #should be ~2000
    for i in range(len(selected_indices)):
        for j in range(len(stardata["kepid"])):
            if str(koimaster["kepid"].iloc[selected_indices[i]]) == str(stardata["kepid"].iloc[j]):
                good_indices.append(j)
                selected_indices[i] = -1
                print("appended " + str(j))
                break
    print(good_indices)
    print(len(good_indices))
    good = False
    for i in range(len(stardata)):
        for j in range(len(good_indices)):
            if i == good_indices[j]:
                good = True
        if good == False:
            bad_indices.append(i)
        good = False
    stardata = stardata.drop(bad_indices)
    stardata = stardata.reset_index(drop=True)
    print("done5")
    print(len(stardata["kepid"])) #should be 2297

    savepath1 = 'data/stardatamodFin.csv'
    savepath2 = 'data/planetdatamodFin.csv'
    stardata.to_csv(savepath1)
    planetdata.to_csv(savepath2)


def compfilter(composite):
    badindices = []
    for i in range(len(composite["fpl_hostname"])):
        if str(composite["fpl_orbper"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fpl_smax"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fpl_eccen"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fpl_eqt"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fst_optmag"].iloc[i]) == "nan" :
            badindices.append(i)
        elif str(composite["fst_nirmag"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fst_spt"].iloc[i]) == "nan" :
            badindices.append(i)
        elif str(composite["fst_teff"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fst_lum"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fst_mass"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fst_rad"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fst_met"].iloc[i]) == "nan":
            badindices.append(i)
        elif str(composite["fst_age"].iloc[i]) == "nan":
            badindices.append(i)
        print(i)

    composite = composite.drop(badindices)
    composite = composite.reset_index(drop=True)
    savepath = 'data/compositeMod.csv'
    composite.to_csv(savepath)
    print(len(composite["fpl_hostname"]))

def trim_stardata(stardata):
    badindices = []
    for i in range(len(stardata["kepid"])):
        if str(stardata["av"].iloc[i]) == "nan":
            print("hi there")
            badindices.append(i)
        print(i)

    stardata = stardata.drop(badindices)
    stardata = stardata.reset_index(drop=True)
    savepath = 'data/keplerstellar_betterMod.csv'
    stardata.to_csv(savepath)
    print(len(stardata["kepid"]))


better_stardata = pd.read_csv("data/keplerstellar-better.csv")
trim_stardata(better_stardata)


