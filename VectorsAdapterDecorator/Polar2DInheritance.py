from Vector2D import Vector2D
import math

class Polar2DInheritance(Vector2D):
    def __init__(self, x, y):
        super().__init__(x, y)

    def getAngle(self):
        x, y = self.getComponents()
        radians = math.atan2(y, x)
        degrees = round(radians * (180 / math.pi), 2)
        return degrees