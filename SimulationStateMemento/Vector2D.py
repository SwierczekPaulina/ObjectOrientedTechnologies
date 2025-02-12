from IVector import IVector
import math

class Vector2D(IVector):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def abs(self):
        return math.hypot(self.x, self.y)

    def cdot(self, param):
        components = param.getComponents()
        return self.x * components[0] + self.y * components[1]

    def getComponents(self):
        return [self.x, self.y]
