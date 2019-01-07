from vpython import *
import math
import numpy as np
from math import radians
from query import *


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
        r1ecliptic.rotate(angle=self.iprime, axis=vector(1, 0, 0))
        r1ecliptic.rotate(angle=self.Oprime, axis=vector(0, 0, 1))
        return r1ecliptic


time = 0
dt = .009
#target sys has to be within compdata set
star = input("Enter a Host Star Name: ")
query = QueryStar(star)
data = query.getResults()
planets = []
ecliptics = []
planetshapes = []
colors = [color.red, color.orange, color.yellow, color.green, color.blue]
starradius = data['star radius'].iloc[0]
planetradii = []
scale = starradius / 10
min_a = 100000

for i in range(len(data['planet name'])):
    if data['a'].iloc[i] < min_a:
        min_a = data['a'].iloc[i]
    planets.append(Spacebody(a = data['a'].iloc[i],
                             e = data['e'].iloc[i],
                             iprime = radians(data['i'].iloc[i])))
    ecliptics.append(vector(0,0,0))
    planetradii.append(data['planet radius'].iloc[i])

for i in range(len(planets)):
    ecliptics[i] = planets[i].update_pos(ecliptics[i], time)
    planetshapes.append(sphere(canvas = scene, pos = ecliptics[i] * 150,
                               radius = (15), color = colors[i]))
    planetshapes[i].trail = curve(canvas = scene, color = colors[i])

starshape = sphere(canvas = scene, pos=vector(0, 0, 0), radius=(25), color=color.yellow)

scene2 = canvas(title='Light Curve',
     width=600, height=200,
     center=vector(5,0,0), background=color.black)
thing = sphere(canvas = scene2, pos = vector(0,0,0), radius = (50), color = color.red)
while True:
    rate(100)
    for i in range(len(planets)):
        ecliptics[i] = planets[i].rotatematrix(ecliptics[i])
        ecliptics[i] = planets[i].update_pos(ecliptics[i], time)
        planetshapes[i].pos = ecliptics[i] * 150
        planetshapes[i].trail.append(pos=planetshapes[i].pos, t=time)
    time = time + dt