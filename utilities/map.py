from math import ceil

from utilities.spatial import Point


MINIMUM_DISTANCE_BETWEEN_OBSTACLES = 10


def get_points_from_tmx(tiled_map):
    ans = []
    for layer in tiled_map.layers:
        if layer.name == "obstacles":
            for obj in layer:
                if hasattr(obj, 'points'):
                    points = obj.points
                    n = len(points)
                    for i in range(-1, n):
                        p1, p2 = Point(points[i]), Point(points[i+1])
                        vector = p2 - p1
                        points_number = ceil(abs(vector) / MINIMUM_DISTANCE_BETWEEN_OBSTACLES)
                        for j in range(points_number):
                            point = p1 + vector * (j / points_number)
                            ans.append((point.x, point.y))

    return ans
