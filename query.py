import numpy as np
import pandas as pd
import os

class QueryCandidates(object):
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
        return stardata, planetdata, koimaster, compdata

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
        return columns

    def get_valid_indices(self, columns): #for given vars, find distinct columns with complete data
        stardata, planetdata, koimaster, compdata = self.start()
        good = True
        indices = []
        for i in range(len(compdata["fpl_hostname"])):
            for col in columns:
                if str(compdata[col].iloc[i]) == 'nan':
                    good = False
            if good:
                indices.append(i)
            good = True
        return indices

    def get_stars_nearby(self, indices): #indices returned from get_valid_indices function
        return "wip"

    def get_m_star(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fst_mass"].iloc[i])
        return data

    def get_r_star(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fst_rad"].iloc[i])
        return data

    def get_m_planet(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fpl_bmasse"].iloc[i])
        return data

    def get_r_planet(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fpl_rade"].iloc[i])
        return data

    def get_d_planet(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fpl_dens"].iloc[i])
        return data

    def get_n_planets(self, indices):
        return "wip"

    def get_eff_temp_star(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fst_teff"].iloc[i])
        return data

    def get_metallicity(self, indices): #check only Fe/H ratio
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fst_met"].iloc[i])
        print(data[:5])
        return data

    def get_period(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fpl_orbper"].iloc[i])
        return data

    def get_vismag(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fst_optmag"].iloc[i])
        return data

    def get_irmag(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fst_nirmag"].iloc[i])
        return data

    def get_a(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fpl_smax"].iloc[i])
        return data

    def get_e(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fpl_eccen"].iloc[i])
        return data

    def get_age(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fst_age"].iloc[i])
        return data

    def get_luminosity(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fst_lum"].iloc[i])
        return data

    def get_spectrum(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(compdata["fst_spt"].iloc[i])
        return data

    def getResults(self):
        stardata,planetdata,koimaster,compdata = self.start()
        columns = self.convert_vars()
        indices = self.get_valid_indices(columns)
        data = []
        coordinates = []
        coord = []
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
        for i in range(len(data[0])):
            coord = []
            for j in range(len(data)):
                coord.append(data[j][i])
            coordinates.append(coord)
        return coordinates


class QueryAll(object): #return dataframe of string planet/noplanet , stellar characteristics all from stardata db
    def __init__(self, vars, filter = False, equalize = False):
        """ Vars is an n-length string list of variables the user wishes to retrieve from the Kepler datasets.
                    included variables:
                    ------------------
                    stars_nearby = number of stars within 3 parsecs of target star
                    ra =  right ascension of target star
                    dec = declination of target star
                    distance = distance of star from earth
                    m_star = mass of star (solar masses)
                    r_star = radius of star (solar radii)
                    d_star = density of star (g/cm^3)
                    n_planets = number of planets in system
                    eff_temp_star = photospheric temperature of star (K)
                    metallicity = stellar metallicity (base-10 logarithm of the Fe to H ratio at the surface of the star,
                                                        normalized by the solar Fe to H ratio)
                    av_extinction = a measure of the absorption and scattering of light in the V-band due to dust and gas
                        in the line of sight
            Filter is a boolean set to true in program building to randomly cut 50% of the data to make processing faster
                    """
        self.vars = vars
        self.filter = filter
        self.equalize = equalize

    def convert_vars(self):
        columns = []
        for var in self.vars:
            if var == "ra":
                columns.append("ra")
            elif var == "dec":
                columns.append("dec")
            elif var == 'distance':
                columns.append("dist")
            elif var == "m_star":
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

    def start(self):
        loadpath1 = 'data/planetdatamod2.csv'
        loadpath2 = 'data/keplerstellar_betterMod.csv'
        loadpath3 = 'data/cumulative.csv'
        loadpath4 = 'data/compositepars.csv'
        planetdata = pd.read_csv(loadpath1, sep=",")
        planetdata = planetdata.reset_index(drop=True)
        stardata = pd.read_csv(loadpath2, sep=",")
        koimaster = pd.read_csv(loadpath3, sep=",")
        compdata = pd.read_csv(loadpath4, sep = ",")

        return stardata, planetdata, koimaster, compdata

    def get_valid_indices(self, columns, type): #for given vars, find distinct columns with complete data
        stardata, planetdata, koimaster, compdata = self.start()
        good = True
        indices = []
        print(columns)
        if type == "planets":
            print("getting planet indices")
            for i in range(len(stardata["kepid"])):
                for col in columns:
                    if str(stardata[col].iloc[i]) == 'nan' or stardata["nkoi"].iloc[i] == 0:
                        good = False
                if good:
                    indices.append(i)
                good = True
        elif type == "noplanets":
            print("getting noplanet indices")
            for i in range(len(stardata["kepid"])):
                for col in columns:
                    if str(stardata[col].iloc[i]) == 'nan' or stardata["nkoi"].iloc[i] != 0:
                        good = False
                if good:
                    indices.append(i)
                good = True
        new_indices = []
        done = False
        j = 30
        if self.filter:
            for i in range(len(indices)):
                if i % 4!= 0:
                    new_indices.append(indices[i])
                if done == False and stardata['nconfp'].iloc[indices[4*j]] != 0:
                    print(stardata.iloc[indices[4*j]])
                    done = True
                j = j + 1
            print("done")
            return new_indices
        else:
            print("donezo")
            return indices

    """def get_stars_nearby(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        hygdata = pd.read_csv('data/stardata_hyg_v2', sep = ",")"""

    def get_ra(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(stardata["ra"].iloc[i])
        return data

    def get_dec(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(stardata["dec"].iloc[i])
        return data

    def get_dist(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(stardata['dist'].iloc[i])
        return data

    def get_m_star(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(stardata["mass"].iloc[i])
        return data

    def get_r_star(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(stardata["radius"].iloc[i])
        return data

    def get_d_star(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(stardata["dens"].iloc[i])
        return data

    def get_n_planets(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        print("getting n_planets")
        for i in indices:
            data.append(stardata["nkoi"].iloc[i])
        return data

    def get_eff_temp_star(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(stardata["teff"].iloc[i])
        return data

    def get_metallicity(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        for i in indices:
            data.append(stardata["feh"].iloc[i])
        return data

    def get_av_extinction(self, indices):
        stardata, planetdata, koimaster, compdata = self.start()
        data = []
        print("getting av extinction")
        for i in indices:
            data.append(stardata["av"].iloc[i])
        return data

    def getResults(self):
        #status of 1 = planets, status of 0 = no planets
        columns = self.convert_vars()
        planet_indices = self.get_valid_indices(columns, type = "planets")
        noplanet_indices = self.get_valid_indices(columns, type = "noplanets")
        new_noplanet_indices = []
        if self.equalize:
            for i in range(len(noplanet_indices)):
                if i <= len(planet_indices):
                    new_noplanet_indices.append(noplanet_indices[i])
        else:
            new_noplanet_indices = noplanet_indices

        data = {'status': []}

        for i in range(len(planet_indices)):
            data['status'].append(1)

        for col in columns:
            if col == "ra":
                data[col] = self.get_ra(planet_indices)
            elif col == "dec":
                data[col] = self.get_dec(planet_indices)
            elif col == 'dist':
                data[col] = self.get_dist(planet_indices)
            elif col == "mass":
                data[col] = self.get_m_star(planet_indices)
            elif col == "radius":
                data[col] = self.get_r_star(planet_indices)
            elif col == "dens":
                data[col] = self.get_d_star(planet_indices)
            elif col == "nkoi":
                data[col] = self.get_n_planets(planet_indices)
            elif col == "teff":
                data[col] = self.get_eff_temp_star(planet_indices)
            elif col == "feh":
                data[col] = self.get_metallicity(planet_indices)
            elif col == "av":
                data[col] = self.get_av_extinction(planet_indices)
            else:
                print("whoops")

        for i in range(len(new_noplanet_indices)):
            data['status'].append(0)

        arr = []
        for col in columns:
            if col == "ra":
                arr = self.get_ra(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            elif col == "dec":
                arr = self.get_dec(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            elif col == 'dist':
                arr = self.get_dist(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            elif col == "mass":
                arr = self.get_m_star(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            elif col == "radius":
                arr = self.get_r_star(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            elif col == "dens":
                arr = self.get_d_star(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            elif col == "nkoi":
                arr = self.get_n_planets(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            elif col == "teff":
                arr = self.get_eff_temp_star(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            elif col == "feh":
                arr = self.get_metallicity(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            elif col == "av":
                arr = self.get_av_extinction(new_noplanet_indices)
                [data[col].append(arr[i]) for i in range(len(arr))]
            else:
                print("whoops")
        formatted_data = pd.DataFrame(data)
        return formatted_data


class QueryStar(object): #uses compdata set
    def __init__(self, star):
        self.star = star

    def start(self):
        loadpath1 = 'data/exomultpars.csv'
        loadpath2 = 'data/stardatamod3.csv'
        loadpath3 = 'data/cumulative.csv'
        loadpath4 = 'data/compositepars.csv'
        planetdata = pd.read_csv(loadpath1, sep=",")
        stardata = pd.read_csv(loadpath2, sep=",")
        koimaster = pd.read_csv(loadpath3, sep=",")
        compdata = pd.read_csv(loadpath4, sep = ",")
        return planetdata, stardata, koimaster, compdata

    def get_valid_indices(self):
        good_indices = []
        planetdata, stardata, koimaster, compdata = self.start()
        for i in range(len(planetdata["mpl_hostname"])):
            if self.star.lower() == str(planetdata["mpl_hostname"].iloc[i]).lower() and planetdata['mpl_def'].iloc[i] == 1:
                good_indices.append(i)
        return good_indices

    def getResults(self):
        planetdata, stardata, koimaster, compdata = self.start()
        good_indices = self.get_valid_indices()
        data = {'planet name': [],
                'discovery method': [],
                'orbital period': [],
                'effective temperature': [],
                'a': [],
                'e': [],
                'i': [],
                'planet radius': [],
                'star radius': []}
        for i in good_indices:
            data['planet name'].append(str(planetdata['mpl_hostname'].iloc[i]) +
                                       str(planetdata['mpl_letter'].iloc[i]))
            data['discovery method'].append(planetdata['mpl_discmethod'].iloc[i])
            if str(planetdata['mpl_orbper'].iloc[i]) == 'nan':
                data['orbital period'].append(100)
            else:
                data['orbital period'].append(planetdata['mpl_orbper'].iloc[i])
            if str(planetdata['mst_teff'].iloc[i]) == 'nan':
                data['effective temperature'].append(5000)
            else:
                data['effective temperature'].append(planetdata['mst_teff'].iloc[i])
            data['a'].append(planetdata['mpl_orbsmax'].iloc[i])
            if str(planetdata['mpl_orbeccen'].iloc[i]) == 'nan':
                data['e'].append(0)
            else:
                data['e'].append(planetdata['mpl_orbeccen'].iloc[i])
            if str(planetdata['mpl_orbincl'].iloc[i]) == 'nan':
                data['i'].append(0)
            else:
                data['i'].append(planetdata['mpl_orbincl'].iloc[i])
            if str(planetdata['mpl_radj'].iloc[i]) == 'nan':
                data['planet radius'].append(planetdata['mpl_orbsmax'].iloc[i]/10)
            else:
                data['planet radius'].append(planetdata['mpl_radj'].iloc[i])
            if str(planetdata['mst_rad'].iloc[i]) == 'nan':
                data['star radius'].append(planetdata['mpl_orbsmax'].iloc[i]/5)
            else:
                data['star radius'].append(planetdata['mst_rad'].iloc[i])
        print(data)
        formatted_data = pd.DataFrame(data)
        return formatted_data






"""query = QueryAll(["n_planets", "av_extinction"], filter = True)
df = query.getResults()
print(len(df))"""

