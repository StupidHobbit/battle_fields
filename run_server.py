import asyncio
from server.game_server import GameHandler
import redis
from server.config import REDIS_SOCKET_PATH


HOST, PORT = "localhost", 1488
PACKET_SIZE = 8096


try:
    r = redis.Redis(unix_socket_path=REDIS_SOCKET_PATH)
except:
    import os
    print('1')
    os.system("redis/src/redis-server ../../redis.conf")
    r = redis.Redis(unix_socket_path=REDIS_SOCKET_PATH)


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