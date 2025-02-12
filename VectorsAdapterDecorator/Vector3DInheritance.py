import math
from Vector2D import Vector2D

class Vector3DInheritance(Vector2D):
    def __init__(self, x, y, z=0):
        super().__init__(x, y)
        self.z = z

    def abs(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def cdot(self, other):
        return super().cdot(other) + self.z * other.z

    def getComponents(self):
        return [self.x, self.y, self.z]

    def cross(self, other):
        x1, y1, z1 = self.getComponents()
        x2, y2, z2 = other.getComponents()

        cross_x = y1 * z2 - z1 * y2
        cross_y = z1 * x2 - x1 * z2
        cross_z = x1 * y2 - y1 * x2

        return Vector3DInheritance(cross_x, cross_y, cross_z)

    def getSrcV(self):
        return Vector2D(self.x, self.y)
