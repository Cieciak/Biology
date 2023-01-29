import threading, time
from ..CPPP import CPPP

HEADER = {'method': 'GET'}
FRAME_BUFFER = []
COUNT = 0

def simulation_loop():
    global COUNT, FRAME_BUFFER
    while True:
        if len(FRAME_BUFFER) < 100:
            FRAME_BUFFER.append({'x': COUNT - 500, 'y': COUNT - 500})
            COUNT = (COUNT + 1) % 1000
        else:
            time.sleep(0.01)

simulation_thread = threading.Thread(target = simulation_loop)
simulation_thread.start()

server = CPPP.CPPPServer('0.0.0.0', 8080)

@server
def handler(requests: CPPP.CPPPMessage):
    global FRAME_BUFFER
    response = CPPP.CPPPMessage(header = HEADER)
    if requests.body == 'get':
        body = FRAME_BUFFER[:10]
        FRAME_BUFFER = FRAME_BUFFER[10:]
        response.add_body(body)
    return response

try: server.serve()
except KeyboardInterrupt: pass