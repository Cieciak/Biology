import threading, time
from ..CPPP import CPPP
from ..utils.math import Vector
from ..utils.being import Being
from ..utils.mendel import Organism, CODONS_DICT

genomes = [
    'CCGAAAAAGAACCACCCTGGCCAACCTACATTT  CCGAACAAGACTAAGAAGTTT   TTCAAGTTT   ATCAAGTTT   CCGCCCAAGAAGTTT   CCGATTCACCACTTT',
    'CCGCATGATCGTCATCGTGATTTT CCGCATCGTGATCATCGTGATTTT  TAATTT TAATTT  TAATTT TAATTT',
    'AAAAGCCAAGGCGTTCGTCCTTGCTTT  CCGTCGTGCGGCAAAATCTCATTT  TTGTTT  AAATTT TCAAAAAGTTTT CCGTGCTGATTT',
    'CCGAAACACCACACGATACACCACTTT  CCGAACAAGTTT  CGACCTTTT  CCGATCATAATACACTTT   TTGAAGTTT  GCTGCATTAGATCACTTT',
]

beings = []
for geneome in genomes:
    beings.append(Being.fromOrganism(Organism.fromDNA(geneome, CODONS_DICT)))

BEING_LIST: list[Being] = beings
FRAME_BUFFER: list[list[Being]] = []

GRAVITY: Vector = Vector(0, 90)

def get_best(beings: list[Being], n: int = 2):
    beings.sort(key = lambda x: x.position.y)
    return beings[:n]

def simulation_loop():
    global BEING_LIST, FRAME_BUFFER
    dt = 1 / 60
    while True:
        if len(FRAME_BUFFER) < 100:
            for obj in BEING_LIST: obj.update(None, dt, external_force = GRAVITY)
            FRAME = [obj.to_dict() for obj in BEING_LIST]
            FRAME_BUFFER += [FRAME, ]
        else:
            time.sleep(0.01)

HEADER = {'method': 'GET'}
COUNT = 0

simulation_thread = threading.Thread(target = simulation_loop)
simulation_thread.start()

server = CPPP.CPPPServer('0.0.0.0', 8080)

@server
def handler(requests: CPPP.CPPPMessage):
    global FRAME_BUFFER, BEING_LIST
    response = CPPP.CPPPMessage(header = HEADER)
    match requests.body:
        case 'get':
            body = FRAME_BUFFER[:10]
            FRAME_BUFFER = FRAME_BUFFER[10:]
            response.add_body(body)
        case 'next_gen':
            P1, P2 = get_best(BEING_LIST)
            BEING_LIST = P1 @ P2
            FRAME_BUFFER = []
        case _:
            print(requests.body)
    return response

try: server.serve()
except KeyboardInterrupt: pass