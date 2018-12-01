import random
import math

class Event:
    time = 0

    def __init__(self, time):
        self.time = time

    def generateTime(self, lamb):
        self.time = ((math.log(random.uniform(0,1)))/(-lamb)) + self.time

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
