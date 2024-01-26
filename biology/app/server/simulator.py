from ...core import Creator
from ..object import Frame, SimObject
from ..math import Vector

from threading import Thread, Event
from time import sleep
from copy import deepcopy

class Simulator:

    def __init__(self, frame_limit: int, creator: Creator):

        # Frame handling
        self.FRAME_LIMIT: int = frame_limit
        self.FRAME_BUFFER: list[Frame] = []
        self.FRAME_THREAD: Thread = Thread(group = None, target = self.loop)
        
        # Control
        self.running: Event = Event()

        # Simulation objects
        self.objects: list[SimObject] = []
        self.creator: Creator = creator

        # Parameters
        self.dt: float = 1 / 60
        self.global_force: Vector = Vector(0, 90)

    def start(self): self.FRAME_THREAD.start()

    def stop(self): self.running.set()

    def loop(self):
        while not self.running.is_set():
            # Check if frame buffer is full, if so skip
            if len(self.FRAME_BUFFER) > self.FRAME_LIMIT:
                sleep(0.01)
                continue
            
            # Add new frame to frame buffer
            frame = self.generate_frame(self.dt)
            self.FRAME_BUFFER += [frame, ]

    def generate_frame(self, dt: float) -> Frame:
        for object in self.objects:
            object.update(dt, self)

        # Have to use deepcopy here to avoid passing by reference
        return Frame(deepcopy(self.objects))
    
    def consume_frames(self, n: int) -> list[Frame]:
        n = min(n, self.FRAME_LIMIT)
        batch             = self.FRAME_BUFFER[:n]
        self.FRAME_BUFFER = self.FRAME_BUFFER[n:]

        return batch
    
    def add_object(self, obj: SimObject): self.objects.append(obj)