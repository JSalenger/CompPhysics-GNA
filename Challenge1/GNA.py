from Exceptions import *
import random

class GNA:

    def __init__(self, dt, familySizes, PopulateCLS, stdDev, callbacks=[], reverseScoring=False):
        # TODO: make pop size variable
        self.populates = []
        self.populationSize = sum(familySizes)
        self.totalTime = 0
        self.dt = 0
        self.familySizes = familySizes
        self.PopulateCLS = PopulateCLS
        self.populatesDead = 0
        self.reverseScoring = reverseScoring
        self.stdDev = stdDev
        self.callbacks = callbacks
        self.epoch = 0


        # assert (len(familySizes) < self.populationSize, "The length of familySizes can not be greater than the population size (the sum of the array)")
        # # might have to wrap in try catch
        # assert (type(PopulateCLS.createNew()) == PopulateCLS, "PopulateCLS.createNew() MUST return an instance of PopulateCLS")
        # assert (type(PopulateCLS.createFrom(PopulateCLS.createNew()) == PopulateCLS, "PopulateCLS.permute MUST return an instance of PopulateCLS")

        for i in range(self.populationSize):
            p = self.PopulateCLS.createNew(dt)
            self.populates.append(p)

    def createNextGeneration(self):
        self.populates.sort(
            key=lambda x: x.getScore(), reverse=self.reverseScoring)
        tempPopulates = []
        for k, familySize in enumerate(self.familySizes):
            for i in range(familySize):
                tempPopulates.append(self.PopulateCLS.createFrom(self.populates[k], self.stdDev))

        print("-----")
        print("Epoch " + str(self.epoch) + " finished.")
        print("Best angle: " + str(self.populates[0].angle))
        print("Slant height: " + str(self.populates[0].position.y))
        print("Loss: " + str(self.populates[0].getScore()))
        print("-----")
        self.epoch += 1

        self.populatesDead = 0

        self.populates = tempPopulates    
    
    def __call__(self):
        for i in self.populates:
            died = i()  # could replace with just "if i()"
            if died:
                self.populatesDead += 1
                print(str(self.populatesDead) + "/" + str(self.populationSize))

        if self.populatesDead == self.populationSize:
            self.createNextGeneration()
            for x in self.callbacks:
                x(self)
        self.totalTime += self.dt
