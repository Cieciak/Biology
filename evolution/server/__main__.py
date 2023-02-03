import threading, time
from ..CPPP import CPPP
from ..utils.math import Vector
from ..utils.being import Being
from ..utils.mendel import Organism, CODONS_DICT

# These are the 4 hand-written starting genomes
ORIGINAL_GENOMES = [
    'CCGAAAAAGAACCACCCTGGCCAACCTACATTT CCGAACAAGACTAAGAAGTTT    TTCAAGTTT ATCAAGTTT          CCGCCCAAGAAGTTT CCGATTCACCACTTT',
    'CCGCATGATCGTCATCGTGATTTT          CCGCATCGTGATCATCGTGATTTT TAATTT    TAATTT             TAATTT          TAATTT',
    'AAAAGCCAAGGCGTTCGTCCTTGCTTT       CCGTCGTGCGGCAAAATCTCATTT TTGTTT    AAATTT             TCAAAAAGTTTT    CCGTGCTGATTT',
    'CCGAAACACCACACGATACACCACTTT       CCGAACAAGTTT             CGACCTTTT CCGATCATAATACACTTT TTGAAGTTT       GCTGCATTAGATCACTTT',
]
# List of currently simulated organisms
BEING_LIST: list[Being] = []
# Generated frames
FRAME_BUFFER: list[list[Being]] = []
FRAME_MAX: int = 100
FRAME_PER_REQUEST: int = 10
# Constant force pulling them down
GRAVITY: Vector = Vector(0, 90)
HEADER = {'method': 'GET'}


def generate_initial_beings(genomes: list[str]):
    return [Being.fromOrganism(Organism.fromDNA(genome, CODONS_DICT)) for genome in genomes]

def get_best(beings: list[Being], n: int = 2):
    beings.sort(key = lambda x: x.position.y)
    return beings[:n]

# Will generate frames
def simulation_loop():
    global BEING_LIST, FRAME_BUFFER, FRAME_MAX
    dt = 1 / 60
    while True:
        if len(FRAME_BUFFER) < FRAME_MAX:
            for obj in BEING_LIST: obj.update(None, dt, external_force = GRAVITY)
            FRAME = [obj.to_dict() for obj in BEING_LIST]
            FRAME_BUFFER += [FRAME, ]
        else:
            time.sleep(0.01)

BEING_LIST = generate_initial_beings(ORIGINAL_GENOMES)


simulation_thread = threading.Thread(target = simulation_loop)
simulation_thread.start()

server = CPPP.CPPPServer('0.0.0.0', 8080)

@server
def handler(requests: CPPP.CPPPMessage):
    global FRAME_BUFFER, BEING_LIST
    response = CPPP.CPPPMessage(header = HEADER)
    match requests.body:
        case 'get':
            body = FRAME_BUFFER[:FRAME_PER_REQUEST]
            FRAME_BUFFER = FRAME_BUFFER[FRAME_PER_REQUEST:]
            response.add_body(body)

        case 'next_gen':
            P1, P2 = get_best(BEING_LIST)
            BEING_LIST = P1 @ P2
            FRAME_BUFFER = []

        case 'regenerate':
            BEING_LIST = generate_initial_beings(ORIGINAL_GENOMES)
            FRAME_BUFFER = []

        case _:
            print(requests.body)
    return response

try: server.serve()
except KeyboardInterrupt: pass