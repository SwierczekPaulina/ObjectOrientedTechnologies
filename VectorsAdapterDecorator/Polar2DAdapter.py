import math
from IVector import IVector
from IPolar2D import IPolar2D

class Polar2DAdapter(IPolar2D, IVector):
    def __init__(self, srcVector):
        self.srcVector = srcVector

    def abs(self):
        return self.srcVector.abs()

    def cdot(self, other):
        return self.srcVector.cdot(other)

    def getComponents(self):
        return [self.abs(), self.getAngle()]

    def getAngle(self):
        x, y = self.srcVector.getComponents()
        radians = math.atan2(y, x)
        degrees = round(radians * (180 / math.pi), 2)
        return degrees