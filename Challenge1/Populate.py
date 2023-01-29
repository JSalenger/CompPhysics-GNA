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

class Populate:
    def __init__(self, angle, gravity, drag, magnus, position=V(0, 0, 0), dt=.1, mass=.045, **kwargs):
        self.angle = angle
        self.position = position
        self.dead = False
        self.velocity = V(330 * math.cos(math.radians(angle)), 330 * math.sin(math.radians(angle)), 0)
        self.sphere = Circle(Point(self.position.x, self.position.y), 5)
        self.sphere.draw(WindowSingleton().instance())
        self.deltaV = 0
        self.deltaP = 0
        self.dt = dt
        self.gravity = gravity
        self.drag = drag
        self.magnus = magnus
        self.mass = mass
    
    @staticmethod
    def createNew(dt=.1):
        mass = 4.2 # kg
        airDensity = .97 # g/m^3
        area = pi*0.125*0.125 #
        Cd = 0.3 # drag coefficient
        g = -9.8 # m/s^2

        gravity = Gravity(g, mass)
        drag = Drag(airDensity, Cd, area)
        magnus = Magnus(5e-5, V(0, 0, 0), V(0, 0, -20), dt)

        theta = random() * 90

        return Populate(theta, gravity, drag, magnus, position=V(30.48 * math.cos(math.radians(theta)), 30.48 * math.sin(math.radians(theta)), 0), dt=dt, mass=mass)   

    @staticmethod
    def createFrom(populate, stdDev):
        theta = gauss(populate.angle, stdDev)

        return Populate(theta, populate.gravity, populate.drag, populate.magnus, V(30.48 * math.cos(math.radians(theta)), 30.48 * math.sin(math.radians(theta)), 0), populate.dt, populate.mass)

        
    def update(self):
        if self.dead:
            return
        
        wind = V(14, 1, 0)

        forces = self.gravity.get() + self.drag.get(self.velocity, wind) # + self.magnus.get(self.velocity, wind) 

        p, v = tick(forces, self.mass, self.velocity, self.position, self.dt)
        self.velocity = v
        self.position = p
                
        if self.position.y < 0:
            self.dead = True
            return True
        else: 
            return False
        
    def display(self):
        self.sphere.move(self.velocity.x * self.dt, self.velocity.y * self.dt)
        
    def __call__(self):
        if self.dead:
            return
        
        died = self.update()
        self.display()
        return died
        
    def getScore(self):
        return self.position.x

    def __del__(self):
        self.sphere.undraw()
