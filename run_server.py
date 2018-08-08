import asyncio
import time
from sys import stdout
import os
from signal import SIG_DFL

import uvloop
import redis

from server.game_server import GameHandler
from server.config import REDIS_SOCKET_PATH


HOST, PORT = "localhost", 1488
PACKET_SIZE = 8096


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if not os.path.exists(REDIS_SOCKET_PATH):
    pid = os.fork()
    if not pid:
        os.system("./run_redis.sh")
        exit(0)

time.sleep(1)
r = redis.Redis(unix_socket_path=REDIS_SOCKET_PATH)
r.flushall()

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(GameHandler, HOST, PORT)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

os.kill(pid, SIG_DFL)
