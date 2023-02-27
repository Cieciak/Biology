import threading, time, random, pprint
from ..CPPP import CPPP
from ..utils.math import Vector
from ..utils.being import Being, PointOfInterest
from ..utils.mendel import Organism, Gene

FRAME_PER_REQUEST = 20
HEADER = {'method': 'GET'}
KERNEL = {0:1, 1:1}
GENES = [
    [Gene.make('COLOR', 2), Gene.make('POLY_TEST', 2, 0)],
    [Gene.make('COLOR', 2), Gene.make('POLY_TEST', 2, 1)],
]

def generate_initial_beings(genes: list[str]):
    output: list[Being] = []
    for genome in genes:
        organism = Organism.fromGenes(genome, KERNEL)
        output += [Being.fromOrganism(organism, Vector(random.randrange(-10, 10), random.randrange(-10, 10))), ]
    pprint.pprint(output)
    return output

class Simulator:

    def __init__(self, frame_limit: int):
        # Frame handling
        self.frame_limit = frame_limit
        self.frame_buffer = []
        self.frame_thread = threading.Thread(group = None, target = self.loop)

        # Simulation objects
        self.objects: list[Being | PointOfInterest] = []

        self.global_force = Vector(0, 90)
        self.dt = 1 / 60
        self.running = threading.Event()

    # Generating new frame
    def frame(self, dt: float):
        new_frame = []
        for obj in self.objects:
            obj.update(self, dt)
            new_frame.append(obj.to_dict())
        return new_frame

    # Consume n frames
    def consume(self, n: int):
        output = self.frame_buffer[:n]
        self.frame_buffer = self.frame_buffer[n:]
        return output

    def clear(self): self.frame_buffer = []

    # Simutation loop
    # runs until frame_limit is reached
    def loop(self):
        while True:
            if self.running.is_set(): return
            if len(self.frame_buffer) > self.frame_limit:
                time.sleep(0.01)
                continue
            frame = self.frame(self.dt)
            self.frame_buffer += [frame, ]

    # Start simulation thread
    def start(self): 
        self.frame_thread.start()

    # Add new objects to simulation
    def add(self, object): self.objects += [object, ]

    # Append list of objects
    def append(self, objects): self.objects += objects

    # Remove all Beings
    def purge(self): self.objects = [obj for obj in self.objects if type(obj) != Being]

    # Filter the objects
    def filter(self, func = None): return filter(func, self.objects)

    # Return the best using filter function 
    def get_best(self, n: int = 2, filter = lambda being: being.position.y):
        beings = [being for being in self.objects if type(being) == Being]
        beings.sort(key = lambda x: min([abs(x.position - poi.position) for poi in self.filter(lambda x: type(x) == PointOfInterest)]))
        return beings[:n]

    # Stop the simulation
    def stop(self): self.running.set()

simulator = Simulator(frame_limit = 100)

poi1 = PointOfInterest(Vector(100, 100), Vector(50, 50), '#FAFF70', 1)
poi2 = PointOfInterest(Vector(-100, 100), Vector(50, 50), '#FAFF70', 2)
poi3 = PointOfInterest(Vector(0, 50), Vector(50, 50), '#FAFF70', 3)

simulator.add(poi1)
simulator.add(poi2)
simulator.add(poi3)

# Add all beings to the simulation
for being in generate_initial_beings(GENES):
    simulator.add(being)

simulator.start()
server = CPPP.CPPPServer('0.0.0.0', 8080)

@server
def handler(requests: CPPP.CPPPMessage):
    global simulator
    response = CPPP.CPPPMessage(header = HEADER)
    match requests.body:
        # GET - Return frames to the sender
        case 'get':
            body = simulator.consume(FRAME_PER_REQUEST)
            response.add_body(body)

        # NEXT_GEN - Make new generation
        case 'next_gen':
            P1, P2 = simulator.get_best()
            F = P1 @ P2
            print(F)
            simulator.purge()
            simulator.append(F)
            simulator.clear()

        # REGENERATE - Regenerate the beings 
        case 'regenerate':
            BEING_LIST = generate_initial_beings(GENES)
            simulator.purge()
            simulator.append(BEING_LIST)
            simulator.clear()

        case _:
            print(requests.body)
    return response

try: server.serve()
except:
    print('Closing server')
    simulator.stop()
    quit()