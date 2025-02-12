from IPolar2D import IPolar2D
import math

class Polar2DAdapter(IPolar2D):
    def __init__(self, srcVector):
        self.srcVector = srcVector

    def abs(self):
        return self.srcVector.abs()

    def getAngle(self):
        x, y = self.srcVector.getComponents()
        return math.atan2(y, x)

    def cdot(self, param):
        return self.srcVector.cdot(param)

    def getComponents(self):
        return self.srcVector.getComponents()

    def setPolarCoordinates(self, magnitude, angle):
        self.srcVector.x = magnitude * math.cos(angle)
        self.srcVector.y = magnitude * math.sin(angle)