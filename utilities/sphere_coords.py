from server.config import EARTH_RADIUS


def get_lon_lat(x, y):
    return x / EARTH_RADIUS, y / EARTH_RADIUS


