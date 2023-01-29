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
        self.velocity = V(80 * math.cos(math.radians(angle)), 80 * math.sin(math.radians(angle)), 0)
        self.sphere = Circle(Point(self.position.x, self.position.y), 1)
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
        mass = 0.045 # kg
        airDensity = 1.2 * math.e ** ((-1.16e-4) * 5) # g/m^3
        area = pi*0.021335*0.021335 #
        Cd = 0.2 # drag coefficient
        g = -9.8 # m/s^2

        gravity = Gravity(g, mass)
        drag = Drag(airDensity, Cd, area)
        # THE MAGNUS FORCE IS NEGATIVE?? ?? ? HELLO ? ?  WHAT? 
        magnus = Magnus(5e-5, V(0, 0, -272), V(0, 0, -20), dt)

        # return Populate(random() * 90, gravity, drag, magnus, dt=dt)
        return Populate(10, gravity, drag, magnus, V(0, 5, 0), dt, mass=mass)
        
    @staticmethod
    def createFrom(populate, stdDev):
        theta = gauss(populate.angle, stdDev)

        return Populate(theta, populate.gravity, populate.drag, populate.magnus, V(30.48 * math.cos(math.radians(theta)), 30.48 * math.sin(math.radians(theta)), 0), populate.dt, populate.mass)

        
    def update(self):
        if self.dead:
            return    
        
        wind = V(-5, 0, 0)
        g = self.gravity.get()
        d = self.drag.get(self.velocity, wind)
        m = self.magnus.get(self.velocity, wind)
        forces = g + d + m
        # print(g, d, m, self.dt)
        # print(forces)

        p, v = tick(forces, self.mass, self.velocity, self.position, self.dt)
        self.velocity = v
        self.position = p

        self.drag.rho = 1.2 * math.e ** ((-1.16e-4)*self.position.y)

                
        if self.position.y < 0:
            self.dead = True
            self.dt = 0
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
                
        return self.position.x

    def __del__(self):
        self.sphere.undraw()
