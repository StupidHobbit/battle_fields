from math import sqrt
class Point:
    __slots__ = ['x', 'y']

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def distance(self, obj):
        return sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)