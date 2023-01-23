import os, threading, json
from ..CPPP import CPPP

KEY_PATH = os.path.dirname(__file__) + '/scp3.keyset'
SERVER = CPPP.SCP3Server.from_keyfile(KEY_PATH, '0.0.0.0', 8000)

def generator(context, x, y):
    return {'x': x, 'y': y}

def generator_loop(context):
    last_x = 0
    last_y = 0
    while True:
        if len(context.queue) < 100:
            context.queue.append(json.dumps(generator(context, last_x, last_y)))
            last_y = (last_x + 1) % 1000 - 500
            last_x = (last_y + 1) % 1000 - 500


@SERVER
def setup(server: CPPP.SCP3Server):
    server.queue: list[dict] = []
    server.generating_thread = threading.Thread(group = None, target = generator_loop, args = (server, ))
    server.generating_thread.start()

@SERVER
def handler(messages: list[bytearray], server: CPPP.SCP3Server):
    output = []
    for message in messages:
        if message.decode('utf-8') == 'give':
            output.append(bytearray(server.queue.pop(0), 'utf-8'))
            print(server.queue)
    return output

SERVER.listen()

try: SERVER.serve()
except KeyboardInterrupt: SERVER.close()
print('Server stopped!')