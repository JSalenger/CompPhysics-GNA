from Populate import Populate
from V import V
from GNA import GNA
from WindowSingleton import WindowSingleton
from graphics import update

position = V(0, 0, 0)
velocity = V(0, 0, 0)
tT = 0

def decreaseDeviationCallback(self):
    self.stdDev /= 2

epoch = 0  
gna = GNA(.01, [45, 25, 15, 9, 6], Populate, 3, [decreaseDeviationCallback], True)


if __name__ == '__main__':
    # DrawBG()
    WindowSingleton()
    while True:
        gna()
        update(24)
