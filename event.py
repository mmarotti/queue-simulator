import randomGen
import math

class Event:
    time = 0
    randomGenerator = randomGen.RandomGenerator()

    def __init__(self, time):
        self.time = time

    def generateTime(self, e):
        randomNumber = self.randomGenerator.generateRandomNumber()
        self.time = ((math.log(randomNumber))/(-1/e)) + self.time

class Arrival(Event):
    def __init__(self, time):
        Event.__init__(self, time)

    def generateTime(self, e):
        Event.generateTime(self, e)

class Exit(Event):
    def __init__(self, time):
        Event.__init__(self, time)

    def generateTime(self, e):
        Event.generateTime(self, e)
