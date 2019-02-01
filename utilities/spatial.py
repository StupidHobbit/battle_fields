from math import sqrt
from dataclasses import dataclass

from scipy.spatial import cKDTree as KDTree


@dataclass
class Point:
    x: float = 0
    y: float = 0

    def distance(self, obj):
        return sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __abs__(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)


class Quadtree:
    def __init__(self):
        pass

    def add_points(self, obj):
        pass
