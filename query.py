import numpy as np
import pandas as pd
import os

class Query(object):
    def __init__(self, vars, checkvalid = False):
        """ Vars is an n-length string list of variables the user wishes to retrieve from the Kepler datasets.
            included variables:
            ------------------
            stars_nearby = number of stars within 3 parsecs of target star
            m_star = mass of star (solar masses)
            r_star = radius of star (solar radii)
            m_planet = mass of planet (jupiter masses)
            r_planet = radius of planet (jupiter radii)
            d_planet = density of planet (g/cm^3)
            n_planets = number of planets in system
            eff_temp_star = effective surface temperature of star (K)
            metallicity = stellar metallicity (base-10 logarithm of the Fe to H ratio at the surface of the star,
                                                normalized by the solar Fe to H ratio)
            period = orbital period of planet (days)
            mag = kepler-band magnitude of star
            semi-major axis = a, in AU
            eccentricity = e
            age = age of star (Gyr)
            luminosity = stellar luminosity (log10(Solar Luminosity))
            spectrum = spectral type"""
        self.vars = vars
        self.composite_params = ["fpl_hostname", "fpl_letter", "fpl_name", "fpl_discmethod", "fpl_orbper", "fpl_smax", "fpl_eccen",
                                 "fpl_bmasse", "fpl_bmassprov", "fpl_rade", "fpl_dens", "fpl_eqt", "fpl_insol", "fst_dist",
                                 "fst_optmag", "fst_optmagband", "fst_nirmag", "fst_nirmagband", "fst_spt", "fst_teff", "fst_logg",
                                 "fst_lum","fst_mass", "fst_rad", "fst_met", "fst_metratio", "fst_age"]
        self.checkvalid = checkvalid

    def start(self):
        loadpath1 = 'data/planetdatamod2.csv'
        loadpath2 = 'data/stardatamod3.csv'
        loadpath3 = 'data/cumulative.csv'
        loadpath4 = 'data/compositepars.csv'
        planetdata = pd.read_csv(loadpath1, sep=",")
        planetdata = planetdata.reset_index(drop=True)
        stardata = pd.read_csv(loadpath2, sep=",")
        koimaster = pd.read_csv(loadpath3, sep=",")
        compdata = pd.read_csv(loadpath4, sep = ",")
        return planetdata,stardata,koimaster, compdata

    def get_matchIndex(self, type, i):
        planetdata,stardata,koimaster, compdata = self.start()
        bufferstring= ""
        point = ""
        zerostring = ""
        koinumber = ""
        if type == "planet":
            print("here")
            point = str(planetdata["mpl_hostname"].iloc[i])
            if str(point)[:3] == "KOI":  # convert to koimaster syntax
                length = len(str(point)[4:])
                bufferstring = "K"
                for j in range(5 - length):
                    zerostring = zerostring + "0"
                zerostring = str(zerostring)
                bufferstring = bufferstring + zerostring
                bufferstring = bufferstring + str(point)[4:]
            for l in range(len(koimaster["kepid"])):
                if "KIC " + str(koimaster["kepid"].iloc[l]) == str(point):
                    koinumber = str(koimaster["kepid"].iloc[l])
                    print("selected1")
                    break
                elif bufferstring == str(koimaster["kepoi_name"].iloc[l])[:6]:
                    koinumber = str(koimaster["kepid"].iloc[l])
                    print("selected2 ", koinumber)
                    break
                elif str(point) + " " + str(planetdata["mpl_letter"].iloc[i]) == str(koimaster["kepler_name"].iloc[l]):
                    koinumber = str(koimaster["kepid"].iloc[l])
                    print("selected3")
                    break
            for m in range(len(stardata["kepid"])):
                if str(stardata["kepid"].iloc[m]) == koinumber:
                    return [i, m]  #planet,star corresponding indices
        else:
            print("whoops")

    def convert_vars(self):
        compindices = []
        for i in self.vars:
            if i == "m_star":
                compindices.append()


    def get_valid_indices(self): #for given vars, find distinct columns with complete data
        stardata, planetdata, koimaster, compdata = self.start()
        for i in range(len(self.vars)):
            for j in range(len(compdata["fpl_hostname"])):




    def get_stars_nearby(self, indices): #indices returned from get_valid_indices function

    def get_m_star(self, indices):

    def get_r_star(self, indices):

    def get_m_planet(self, indices):

    def get_r_planet(self, indices):

    def get_d_planet(self, indices):

    def get_n_planets(self, indices):

    def get_eff_temp_star(self, indices):

    def get_metallicity(self, indices): #check only Fe/H ratio

    def get_period(self, indices):

    def get_mag(self, indices):

    def get_a(self, indices):

    def get_e(self, indices):

    def get_age(self, indices):

    def get_luminosity(self, indices):

    def get_spectrum(self, indices):

    def getResults(self):





query = Query(["metallicity, eff_temp"])
indices = query.get_matchIndex("planet", 67)
planetdata,stardata, koimaster= query.start()
print(indices)
print(planetdata["mst_mass"].iloc[indices[0]])
print(stardata["mass"].iloc[indices[1]])

