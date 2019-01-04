from vpython import *
import math
import numpy as np
from math import radians


class Spacebody(object):
    def __init__(self, a, e, iprime):
        self.a = a
        self.e = e
        self.M = radians(336.0050001501443)
        self.Oprime = radians(108.032597191534)
        self.iprime = iprime
        self.wprime = radians(74.95130563682554)

    def solvekep(self, Mt):
        Eguess = Mt
        Mguess = Eguess - (self.e) * sin(Eguess)
        Mtrue = Mt
        while abs(Mguess - Mtrue) > 1e-4:  # reverse condition
            Eguess = Eguess - (
            (Eguess - (self.e) * sin(Eguess) - Mtrue) / (1 - (self.e) * cos(Eguess)))  # flipped two minus
            Mguess = Eguess - (self.e) * sin(Eguess)
        return Eguess

    def update_pos(self, r1ecliptic, t):
        mu = 1
        period = math.sqrt(4 * pi ** 2 * (self.a) ** 3 / mu)
        Mtrue = 2 * pi / period * (t) + self.M
        Etrue = self.solvekep(Mtrue)
        r1ecliptic.x = (self.a) * math.cos(Etrue) - ((self.a) * (self.e))
        r1ecliptic.y = (self.a) * math.sqrt(1 - (self.e) ** 2) * math.sin(Etrue)
        r1ecliptic.z = 0
        return r1ecliptic

    def rotatematrix(self, r1ecliptic):
        r1ecliptic.rotate(angle=-self.wprime, axis=vector(0, 0, 1))
        print(r1ecliptic)
        r1ecliptic.rotate(angle=self.iprime, axis=vector(1, 0, 0))
        print(r1ecliptic)
        r1ecliptic.rotate(angle=self.Oprime, axis=vector(0, 0, 1))
        return r1ecliptic

#target sys has to be within compdata set


time = 0
dt = .009

asteroid = Spacebody(a=2.773017979589484, e=0.1750074901308245,
                     iprime=radians(16.34548466739393))
mercury = Spacebody(a=0.38709893, e=0.20563069,
                    iprime=radians(7.00487))
venus = Spacebody(a=0.72333199, e=0.00677323,
                  iprime=radians(3.39471))
earth = Spacebody(a=1.00000011, e=0.01671022,
                  iprime=radians(0.00005))
mars = Spacebody(a=1.52366231, e=0.09341233,
                 iprime=radians(1.85061))

ast_ecliptic = vector(0, 0, 0)
mercury_ecliptic = vector(0, 0, 0)
venus_ecliptic = vector(0, 0, 0)
earth_ecliptic = vector(0, 0, 0)
mars_ecliptic = vector(0, 0, 0)

ast_ecliptic = asteroid.update_pos(ast_ecliptic, time)
mercury_ecliptic = mercury.update_pos(mercury_ecliptic, time)
venus_ecliptic = venus.update_pos(venus_ecliptic, time)
earth_ecliptic = earth.update_pos(earth_ecliptic, time)
mars_ecliptic = mars.update_pos(mars_ecliptic, time)

asteroid_geo = sphere(canvas = scene, pos=ast_ecliptic * 150, radius=(15), color=color.white)
mercury_geo = sphere(canvas = scene, pos=mercury_ecliptic * 150, radius=(10), color=color.red)
venus_geo = sphere(canvas = scene, pos=venus_ecliptic * 150, radius=(10), color=color.orange)
earth_geo = sphere(canvas = scene, pos=earth_ecliptic * 150, radius=(10), color=color.green)
mars_geo = sphere(canvas = scene, pos=mars_ecliptic * 150, radius=(10), color=color.blue)

asteroid_geo.trail = curve(canvas = scene, color=color.white)
mercury_geo.trail = curve(canvas = scene, color=color.red)
venus_geo.trail = curve(canvas = scene, color=color.orange)
earth_geo.trail = curve(canvas = scene, color=color.green)
mars_geo.trail = curve(canvas = scene, color=color.blue)

sun = sphere(canvas = scene, pos=vector(0, 0, 0), radius=(25), color=color.yellow)

scene2 = canvas(title='Light Curve',
     width=600, height=200,
     center=vector(5,0,0), background=color.black)
thing = sphere(canvas = scene2, pos = vector(0,0,0), radius = (50), color = color.red)
while True:
    rate(50)
    ast_ecliptic = asteroid.rotatematrix(ast_ecliptic)
    ast_ecliptic = asteroid.update_pos(ast_ecliptic, time)
    asteroid_geo.pos = ast_ecliptic * 150
    asteroid_geo.trail.append(pos=asteroid_geo.pos, t=time)

    mercury_ecliptic = mercury.rotatematrix(mercury_ecliptic)
    mercury_ecliptic = mercury.update_pos(mercury_ecliptic, time)
    mercury_geo.pos = mercury_ecliptic * 150
    mercury_geo.trail.append(pos=mercury_geo.pos, t=time)

    venus_ecliptic = venus.rotatematrix(venus_ecliptic)
    venus_ecliptic = venus.update_pos(venus_ecliptic, time)
    venus_geo.pos = venus_ecliptic * 150
    venus_geo.trail.append(pos=venus_geo.pos, t=time)

    earth_ecliptic = earth.rotatematrix(earth_ecliptic)
    earth_ecliptic = earth.update_pos(earth_ecliptic, time)
    earth_geo.pos = earth_ecliptic * 150
    earth_geo.trail.append(pos=earth_geo.pos, t=time)

    mars_ecliptic = mars.rotatematrix(mars_ecliptic)
    mars_ecliptic = mars.update_pos(mars_ecliptic, time)
    mars_geo.pos = mars_ecliptic * 150
    mars_geo.trail.append(pos=mars_geo.pos, t=time)
    time = time + dt