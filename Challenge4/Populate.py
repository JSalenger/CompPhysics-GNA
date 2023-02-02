from V import V
import math
from random import gauss, random
from Engine import tick
from WindowSingleton import WindowSingleton
from Drag import Drag
from Gravity import Gravity
from graphics import Circle, Point
from Magnus import Magnus
from math import pi

def airDensity(y):
    if y < 11000:
        T = 15.04 - .00649 * y
        p = 101.29 * ((T + 273.1)/(288.08))**5.256

        rho = (p) / (.2869 * (T + 273.1))

        return rho
    
    if 11000 < y < 25000:
        T = -56.46
        p = 22.65 * math.e**(1.73 - .000157 * y)

        rho = (p) / (.2869 * (T + 273.1))

        return rho
    
    if y > 25000:
        T = -131.21 + .00299 * y
        p = 2.488 * ((T + 273.1)/(216.6))**(-11.388)

        rho = (p) / (.2869 * (T + 273.1))

        return rho

class Populate:
    def __init__(self, speed, gravity, drag, magnus, position=V(0, 0, 0), dt=.1, mass=.045, **kwargs):
        self.angle = 90
        self.position = position
        self.dead = False
        self.speed = speed
        self.velocity = V(0, speed, 0)
        self.sphere = Circle(Point(self.position.x, self.position.y), 1)
        self.sphere.draw(WindowSingleton().instance())
        self.deltaV = 0
        self.deltaP = 0
        self.dt = dt
        self.gravity = gravity
        self.drag = drag
        self.magnus = magnus
        self.mass = mass
        self.maxDrag = (0, 0)
        self.totalTime = 0
    
    @staticmethod
    def createNew(dt=.1):
        mass = 15 # kg
        area = pi*0.08*0.08 #
        Cd = 0.5 # drag coefficient
        g = -9.8 # m/s^2

        gravity = Gravity(g, mass)
        drag = Drag(airDensity(0), Cd, area)
        magnus = Magnus(5e-5, V(0, 0, -240), V(0, 0, -20), dt)

        # return Populate(random() * 90, gravity, drag, magnus, dt=dt)
        return Populate(4000, gravity, drag, magnus, V(0, 8_848.86, 0), dt, mass=mass)
        
    @staticmethod
    def createFrom(populate, stdDev):
        speed = gauss(populate.speed, stdDev)

        return Populate(speed, populate.gravity, populate.drag, populate.magnus, V(0, 8_848.86, 0), populate.dt, populate.mass)

        
    def update(self):
        if self.dead:
            return    
        
        wind = V(0, 0, 0)

        self.drag.rho = airDensity(self.position.y)


        d = self.drag.get(self.velocity, wind)
        forces = self.gravity.get() + d # + self.magnus.get(self.velocity, wind))

        if d.m > self.maxDrag[0]:
            self.maxDrag = (d.m, self.totalTime)


        p, v = tick(forces, self.mass, self.velocity, self.position, self.dt)
        self.velocity = v
        self.position = p

        self.totalTime += self.dt
                
        if self.velocity.y < 0:
            self.dead = True
            return True
        else: 
            return False
        
    def display(self):
        self.sphere.move(self.velocity.x * self.dt, self.velocity.y * self.dt)
        
    def __call__(self):
        died = self.update()
        self.display()
        return died
        
    def getScore(self):
        goal = V(164, 0, 0)
        distance = V(self.position.y, self.position.x, 0).m

        if self.position.y < 100000:
            return float('inf')
                
        return self.speed

    def __del__(self):
        self.sphere.undraw()
