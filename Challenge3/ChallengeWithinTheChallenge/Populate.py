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
    def __init__(self, time, gravity, drag, magnus, position=V(0, 0, 0), dt=.1, mass=.045, **kwargs):
        self.angle = 20
        self.position = position
        self.dead = False
        self.velocity = V(0, 0, 60)
        self.sphere = Circle(Point(self.position.x, self.position.y), 1)
        self.sphere.draw(WindowSingleton().instance())
        self.deltaV = 0
        self.deltaP = 0
        self.dt = dt
        self.gravity = gravity
        self.drag = drag
        self.magnus = magnus
        self.mass = mass
        self.time = time
    
    @staticmethod
    def createNew(dt=.1):
        mass = 0.6 # kg
        airDensity = 1.2 # g/m^3
        area = pi*0.12*0.12 #
        Cd = 0.5 # drag coefficient
        g = -9.8 # m/s^2

        gravity = Gravity(g, mass)
        drag = Drag(airDensity, Cd, area)
        magnus = Magnus(5e-5, V(0, 0, -240), V(0, 0, -20), dt)

        time = (random() * 5) - 2.5

        return Populate(time, gravity, drag, magnus, V(-38.75, 96.952, time * 60), dt, mass=mass)
        
    @staticmethod
    def createFrom(populate, stdDev):
        time = gauss(populate.time, stdDev)

        return Populate(time, populate.gravity, populate.drag, populate.magnus, V(-38.75, 96.952, time * 60), populate.dt, populate.mass)

        
    def update(self):
        if self.dead:
            return    
        
        wind = V(10 * math.cos(math.radians(40)), 0, 10 * math.sin(math.radians(40)))

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
        died = self.update()
        self.display()
        return died
        
    def getScore(self):
        goal = V(164, 0, 0)
        distance = V(self.position.y, self.position.x, 0).m
                
        return (V(0, 0, 0) - self.position).m

    def __del__(self):
        self.sphere.undraw()
