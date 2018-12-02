import randomGen
import math

class Event:
    time = 0
    randomGenerator = randomGen.RandomGenerator(351)

    def __init__(self, time):
        self.time = time

    def generateTime(self, lamb):
        randomNumber = self.randomGenerator.generateRandomNumber()
        self.time = ((math.log(randomNumber))/(-lamb)) + self.time

class Arrival(Event):
    def __init__(self, time):
        Event.__init__(self, time)

    def generateTime(self, lamb):
        Event.generateTime(self, lamb)

class Exit(Event):
    def __init__(self, time):
        Event.__init__(self, time)

    def generateTime(self, lamb):
        Event.generateTime(self, lamb)
