from multiprocessing.dummy import Pool
from time import time, sleep

import redis
from scipy.spatial import cKDTree

from server.config import REDIS_SOCKET_PATH, TURN_DELAY
from utilities.sphere_coords import get_lon_lat
from utilities.map import get_points_from_tmx
from resources import tiled_map


class Game:
    def __init__(self):
        self.pool = Pool(5)
        self.r = redis.Redis(unix_socket_path=REDIS_SOCKET_PATH, decode_responses=True)
        self.units_names = set()
        self.p = self.r.pubsub(ignore_subscribe_messages=True)
        self.p.subscribe(**{'new_units': self.handle_new_unit})
        self.p.subscribe(**{'deleted_units': self.handle_deleted_unit})
        self.obstacles = cKDTree(get_points_from_tmx(tiled_map))

    def handle_new_unit(self, message):
        self.units_names.add(message['data'])
        print('New unit with name %s created' % message['data'])

    def handle_deleted_unit(self, message):
        self.units_names.remove(message['data'])
        print('New unit with name %s deleted' % message['data'])

    def update_unit(self, unit_name):
        #self.  r.pipeline()
        unit = self.r.hmget(unit_name, ['x', 'y', 'dx', 'dy'])
        unit = list(map(float, unit))
        x = unit[0] + self.dt * unit[2]
        y = unit[1] + self.dt * unit[3]
        new_unit = {
            'x': x,
            'y': y
        }
        if len(self.obstacles.query_ball_point([x, y], 16)):
            pass
            #new_unit['x'] = unit[0]
            #new_unit['y'] = unit[1]
            #new_unit['dx'] = 0
            #new_unit['dy'] = 0
        else:
            self.r.geoadd('map', *get_lon_lat(x, y), unit_name[4:])
            self.r.hmset(unit_name, new_unit)

    def run_forever(self):
        last_time = time()
        while True:
            cur_time = time()
            self.dt = cur_time - last_time
            last_time = cur_time
            self.p.get_message()
            t = self.pool.map(self.update_unit, self.units_names)
            sleep(max(TURN_DELAY - time() + last_time, 0))


    def shutdown(self):
        self.p.close()
        self.pool.close()
        self.pool.join()


if __name__ == '__main__':
    pass