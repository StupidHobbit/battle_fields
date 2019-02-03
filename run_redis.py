import os
import time

import redis

from server.config import REDIS_SOCKET_PATH


if not os.path.exists(REDIS_SOCKET_PATH):
    os.system("redis/src/redis-server redis.conf")
