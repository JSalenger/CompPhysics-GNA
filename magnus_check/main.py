from Populate import Populate
from V import V
from GNA import GNA
from WindowSingleton import WindowSingleton
from graphics import update as refresh
from time import time

position = V(0, 0, 0)
velocity = V(0, 0, 0)
tT = 0

def decreaseDeviationCallback(self):
    self.stdDev /= 2

epoch = 0  
gna = GNA(.0001, [1], Populate, 3, [decreaseDeviationCallback], True)

def update():
    """ Will be called as many times as possible. """
    gna()

    return

def fixedUpdate():
    """ Will be called at most _FPS number of times per second. Put costly graphics operations in here. """
    refresh()

    return


if __name__ == '__main__':
    # DrawBG()
    WindowSingleton()

    # TODO: only add drawing changes to callstack when update is about to be called
    timeSinceUpdate = time()
    _FPS = 30
    _SPF = 1/_FPS # seconds per frame refresh


    while True:
        update()

        if time() - timeSinceUpdate > _SPF:
            timeSinceUpdate = time()
            fixedUpdate()
            



        
