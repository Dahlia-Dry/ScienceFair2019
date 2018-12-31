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
            vismag = optical magnitude of star
            irmag = infrared magnitude of star
            semi-major axis = a, in AU
            eccentricity = e
            age = age of star (Gyr)
            luminosity = stellar luminosity (log10(Solar Luminosity))
            spectrum = spectral type"""
        self.vars = vars
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
        columns = []
        for i in self.vars:
            if i == "m_star":
                columns.append("fst_mass")
            elif i== "r_star":
                columns.append("fst_rad")
            elif i == "m_planet":
                columns.append("fpl_bmasse")
            elif i == "r_planet":
                columns.append("fpl_rade")
            elif i == "d_planet":
                columns.append("fpl_dens")
            elif i == "n_planets":
                columns.append("") ####
            elif i == "eff_temp_star":
                columns.append("fst_teff")
            elif i == "metallicity":
                columns.append("fst_met")
            elif i == "period":
                columns.append("fpl_orbper")
            elif i == "vismag":
                columns.append("fst_optmag")
            elif i == "irmag":
                columns.append("fst_nirmag")
            elif i == "semi-major axis":
                columns.append("fpl_smax")
            elif i == "eccentricity":
                columns.append("fpl_eccen")
            elif i == "age":
                columns.append("fst_age")
            elif i == "luminosity":
                columns.append("fst_lum")
            elif i == "spectrum":
                columns.append("fst_spt")
            else:
                print("sorry")
        return(columns)

    def get_valid_indices(self, columns): #for given vars, find distinct columns with complete data
        stardata, planetdata, koimaster, compdata = self.start()
        good = True
        for i in range(len(compdata["fpl_hostname"])):
            for col in columns:
                if str(compddata[col].iloc[i]) == 'nan':
                    good = False
            if good:
                indices.append(i)
            good = True
        return indices

    def get_stars_nearby(self, indices): #indices returned from get_valid_indices function
        return "wip"

    def get_m_star(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        m_star = []
        for i in indices:
            m_star.append(compdata[])

    def get_r_star(self, indices):

    def get_m_planet(self, indices):

    def get_r_planet(self, indices):

    def get_d_planet(self, indices):

    def get_n_planets(self, indices):

    def get_eff_temp_star(self, indices):

    def get_metallicity(self, indices): #check only Fe/H ratio

    def get_period(self, indices):

    def get_vismag(self, indices):

    def get_irmag(self, indices):

    def get_a(self, indices):

    def get_e(self, indices):

    def get_age(self, indices):

    def get_luminosity(self, indices):

    def get_spectrum(self, indices):

    def getResults(self):
        stardata,planetdata,koimaster,compdata = self.start()
        columns = self.convert_vars()
        indices = self.get_valid_indices(columns)
        data = []
        for col in columns:
            if col == "fst_mass":
                data.append(self.get_m_star(indices))
            elif col == "fst_rad":
                data.append(self.get_r_star(indices))
            elif col == "fpl_bmasse":
                data.append(self.get_m_planet(indices))
            elif col == "fpl_rade":
                data.append(self.get_r_planet(indices))
            elif col == "fpl_dens":
                data.append(self.get_d_planet(indices))
            elif col == "fst_teff":
                data.append(self.get_eff_temp_star(indices))
            elif col == "fst_met":
                data.append(self.get_metallicity(indices))
            elif col == "fpl_orbper":
                data.append(self.get_period(indices))
            elif col == "fst_optmag":
                data.append(self.get_vismag(indices))
            elif col == "fst_nirmag":
                data.append(self.get_irmag(indices))
            elif col == "fpl_smax":
                data.append(self.get_a(indices))
            elif col == "fpl_eccen":
                data.append(self.get_e(indices))
            elif col == "fst_age":
                data.append(self.get_age(indices))
            elif col == "fst_lum":
                data.append(self.get_luminosity(indices))
            elif col == "fst_spt":
                data.append(self.get_spectrum(indices))
            elif col == "":
                print("wip")
            else:
                print("whoops")







query = Query(["metallicity, eff_temp"])
indices = query.get_matchIndex("planet", 67)
planetdata,stardata, koimaster= query.start()
print(indices)
print(planetdata["mst_mass"].iloc[indices[0]])
print(stardata["mass"].iloc[indices[1]])

