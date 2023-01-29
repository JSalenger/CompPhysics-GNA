from V import V
import math
from random import gauss, random
from Engine import tick
from WindowSingleton import WindowSingleton
from Drag import Drag
from Gravity import Gravity
from graphics import Circle, Point
from math import pi

class Populate:
    def __init__(self, speed, gravity, drag, magnus, position=V(0, 0, 0), dt=.1, mass=.045, **kwargs):
        self.angle = 54
        self.position = position
        self.speed = speed
        self.dead = False
        self.velocity = V(speed * math.cos(math.radians(self.angle)), speed * math.sin(math.radians(self.angle)), 0)
        self.sphere = Circle(Point(self.position.x, self.position.y), 1)
        self.sphere.draw(WindowSingleton().instance())
        self.deltaV = 0
        self.deltaP = 0
        self.dt = dt
        self.gravity = gravity
        self.drag = drag
        self.magnus = magnus
        self.mass = mass
        self.hitHill = False
    
    @staticmethod
    def createNew(dt=.1):
        mass = 0.045 # kg
        airDensity = 0 # g/m^3
        area = pi*0.021335*0.021335 #
        Cd = 0.2 # drag coefficient
        g = -1.62 # m/s^2

        gravity = Gravity(g, mass)
        # drag = Drag(airDensity, Cd, area)
        # magnus = Magnus(5e-5, V(0, 0, -240), V(0, 0, -20), dt)

        return Populate(random() * 20, gravity, None, None, dt=dt)
        
    @staticmethod
    def createFrom(populate, stdDev):
        theta = gauss(populate.speed, stdDev)

        return Populate(theta, populate.gravity, populate.drag, populate.magnus, dt=populate.dt, mass=populate.mass)

        
    def update(self):
        if self.dead:
            return    
        
        wind = V(0, 0, 0)

        forces = self.gravity.get() # + self.drag.get(self.velocity, wind) + self.magnus.get(self.velocity, wind)

        p, v = tick(forces, self.mass, self.velocity, self.position, self.dt)
        self.velocity = v
        self.position = p

        def f(x, y): return (x-100)*(x-100) + y*y

        if (self.position.y < 0 and self.position.x <= 50) or (f(self.position.x, self.position.y) <= 2500 and self.position.x >= 50 and self.position.x <= 150) or (self.position.y <= 0 and self.position.x >= 150):
            self.dead = True
            if (f(self.position.x, self.position.y) <= 2500 and self.position.x >= 50 and self.position.x <= 150) or (self.position.y < 0 and self.position.x <= 50):
                self.hitHill = True

            return True
        else: 
            return False
        
    def display(self):
        self.sphere.move(self.velocity.x * self.dt, self.velocity.y * self.dt)
        
    def __call__(self):
        died = self.update()

        if not self.dead:
            self.display()

        return died
        
    def getScore(self):
        goal = V(164, 0, 0)
        distance = V(self.position.y, self.position.x, 0).m

        if self.hitHill:
            return float('-inf')

        return 0 - self.speed

    def __del__(self):
        self.sphere.undraw()
