import math
from IVector import IVector

class Vector2D(IVector):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def abs(self):
        return math.sqrt(self.x**2 + self.y**2)

    def cdot(self, other):
        components = other.getComponents()
        return self.x * components[0] + self.y * components[1]

    def getComponents(self):
        return [self.x, self.y]