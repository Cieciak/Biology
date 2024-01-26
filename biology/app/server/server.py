from ..object import Dummy, Frame, Being
from ..math import Vector

from .simulator import Simulator

from ...core import Creator

import CPPP

import pickle, random, base64

def init(ctx: CPPP.Context):
    ...

def info(*args, **kwargs) -> CPPP.Message:
    return CPPP.Message.response(b'This is Evolution Server')

def brown(d: Dummy, t: float, s) -> Dummy:
    d.position += Vector(
        x = 2 * random.random() - 1,
        y = 2 * random.random() - 1,
    )

    return d

class Server:
    
    def __init__(self, creator: Creator, objects: list = None):
        if objects is None: objects = []

        # CPPP Server
        self.CP3_server = CPPP.Server('0.0.0.0', 8080)

        self.CP3_server(init)
        self.CP3_server.handler('INFO')(info)
        self.CP3_server.handler('GET-FRAME')(self.frame)
        self.CP3_server.handler('NEXT-GENERATION')(self.generation)

        # Simulator
        self.simulator = Simulator(100, creator)

        for obj in objects:
            self.simulator.add_object(obj)

        self.simulator.start()

    def frame(self, sock, msg: CPPP.Message, server: CPPP.Server) -> CPPP.Message:

        frame = self.simulator.consume_frames(20)
        data = base64.b64encode(pickle.dumps(frame))
        return CPPP.Message(head = {'method': 'RESPONSE'}, body = data)
    
    def generation(self, sock, msg: CPPP.Message, server: CPPP.Server) -> CPPP.Message:

        beings = [obj for obj in self.simulator.objects if type(obj) is Being]

        P1, P2 = random.choices(beings, k = 2)

        F = P1.breed(P2, self.simulator.creator)

        self.simulator.objects = F


    def serve(self):
        self.CP3_server.serve()