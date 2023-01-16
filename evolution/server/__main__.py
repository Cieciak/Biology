import os, threading
from ..CPPP import CPPP

KEY_PATH = os.path.dirname(__file__) + '/scp3.keyset'
SERVER = CPPP.SCP3Server.from_keyfile(KEY_PATH, '0.0.0.0', 8000)

def generator(context):
    last = 0
    while len(context) <= 100:
        context.append(last)
        last += 1

def generator_loop(context):
    while True:
        generator(context)

@SERVER
def setup(server: CPPP.SCP3Server):
    server.queue = []
    server.generating_thread = threading.Thread(group = None, target = generator_loop, args = (server.queue ,))
    server.generating_thread.start()

@SERVER
def handler(messages: list[bytearray], server: CPPP.SCP3Server):
    output = []
    for message in messages:
        if message.decode('utf-8') == 'give':
            output.append(bytearray(str(server.queue.pop(0)), 'utf-8'))
            print(server.queue)
    return output

SERVER.listen()

try: SERVER.serve()
except KeyboardInterrupt: SERVER.close()
print("Server stopped!")