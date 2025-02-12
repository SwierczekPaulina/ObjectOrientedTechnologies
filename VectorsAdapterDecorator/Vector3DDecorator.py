import math
from IVector import IVector
from Vector2D import Vector2D

class Vector3DDecorator(IVector):
    def __init__(self, srcVector, z=0):
        self.srcVector = srcVector
        self.z = z

    def abs(self):
        return math.sqrt(self.srcVector.abs()**2 + self.z**2)

    def cdot(self, other):
        components = other.getComponents()
        return self.srcVector.cdot(other) + self.z * components[2]

    def getComponents(self):
        return self.srcVector.getComponents() + [self.z]

    def cross(self, other):
        x1, y1, _ = self.getComponents()
        x2, y2, _ = other.getComponents()
        z_cross = x1 * y2 - y1 * x2
        return Vector3DDecorator(Vector2D(0, 0), z_cross)
    
    def getSrcV(self):
        return self.srcVector
