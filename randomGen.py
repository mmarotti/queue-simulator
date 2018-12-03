from datetime import datetime

class RandomGenerator:
	m = 2**48
	a = 25214903917
	c = 11
	def __init__(self, seed):
		self.lastGenerated = seed

	def __init__(self):
		time = datetime.now()
		seed = time.microsecond
		self.lastGenerated = seed

	def generateRandomNumber(self):
		randomNumber = (self.a*self.lastGenerated + self.c)%self.m
		self.lastGenerated = randomNumber
		return(randomNumber/self.m)