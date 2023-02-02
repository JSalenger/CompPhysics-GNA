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
    def __init__(self, speed, gravity, drag, magnus, position=V(0, 0, 0), dt=.1, mass=.045, acceptableMiss=5, **kwargs):
        self.angle = 14
        self.position = position
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
        self.speed = speed
        self.acceptableMiss = 5
    
    @staticmethod
    def createNew(dt=.1):
        mass = 0.045 # kg
        airDensity = 1.2 # g/m^3
        area = pi*0.021335*0.021335 #
        Cd = 0.2 # drag coefficient
        g = -9.8 # m/s^2

        gravity = Gravity(g, mass)
        drag = Drag(airDensity, Cd, area)
        magnus = Magnus(3e-5, V(0, 0, -500), V(0, 0, -60), dt)

        # return Populate(random() * 90, gravity, drag, magnus, dt=dt)
        return Populate(random() * 90, gravity, drag, magnus, V(0, 0, 0), dt, mass=mass)
        
    @staticmethod
    def createFrom(populate, stdDev):
        speed = gauss(populate.speed, stdDev)
        magnus = Magnus(3e-5, V(0, 0, -500), V(0, 0, -60), .001)

        return Populate(speed, populate.gravity, populate.drag, magnus, V(0, 0, 0), populate.dt, populate.mass, max(populate.acceptableMiss /  2, 1))

        
    def update(self):
        if self.dead:
            return    
        
        wind = V(5, 0, 0)

        forces = self.gravity.get() + self.drag.get(self.velocity, wind) + self.magnus.get(self.velocity, wind)

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

        goal = V(180, 0, 0)
        if abs((goal - self.position).m) > self.acceptableMiss:
            return (True, self.velocity.x)
        else:
            # hit the goal
            return (False, self.velocity.x)

    def __del__(self):
        self.sphere.undraw()
