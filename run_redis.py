import os
import time

import redis

from server.config import REDIS_SOCKET_PATH


if not os.path.exists(REDIS_SOCKET_PATH):
    os.system("redis/src/redis-server redis.conf")

time.sleep(1)
r = redis.Redis(unix_socket_path=REDIS_SOCKET_PATH)
r.flushall()