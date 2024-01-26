from ...core import Organism, Creator
from ..math import Vector
from math import exp

from tkinter import Canvas
from typing import Any, Self

class Being:

    @staticmethod
    def time_coeff(t: float) -> float:
        'Force `t` seconds after using wings'
        return exp(-(4*t-2)**2)
    
    @classmethod
    def fromOrganism(cls, organism: Organism, position: Vector(0, 0), pmap: dict, creator: Creator):
        default = {
            'position': position,
            'mass': 1.0,
            'wing_force': Vector(0, 240),
            'size': Vector(40, 40),
        }

        properties = creator.make(organism.executable)

        for index, prop in pmap.items():
            name, typ = prop
            match typ: 
                case 'scale':
                    default[name] *= 1.2 ** properties[index]
                case 'add':
                    default[name] += properties[index]

        being = cls()
        being.organism = organism
        being.pmap = pmap

        for key, value in default.items():
            setattr(being, key, value)

        return being

    def __init__(self, 
                 mass: float = 1.0,
                 position: Vector = Vector(0, 0),
                 acceleration: Vector = Vector(0,0),
                 velocity: Vector = Vector(0, 0),
                 force: Vector = Vector(0, 0)):
        
        # Physics
        self.mass: float = mass # [kg]
        self.position: Vector = position #[m]
        self.acceleration: Vector = acceleration #[m/s**2]
        self.velocity: Vector = velocity # [m/s]
        self.force: Vector = force # [N]

        # Biology
        self.wing_force: Vector = Vector(0, 240) # [N]
        self.size: Vector = Vector(40, 40)
        self.last_flap: float = 1e10 # [s]

        self.pmap: dict = {}
        self.organism: Organism = None # Created by default means

    def breed(self, other: Self, creator: Creator) -> list[Self]:

        P1 = self.organism
        P2 = other.organism

        F = P1 @ P2

        return [Being.fromOrganism(org, Vector(0, 0), self.pmap, creator) for org in F]

    def make_decision(self, dt: float, sim: Any):

        trigger = (self.position.y  + 1 * self.velocity.y) > 0

        if trigger and self.last_flap > 1: self.last_flap = 0

    def update(self, dt: float, sim: Any):
        self.make_decision(dt, sim)

        external_force = sim.global_force
        
        self.force = -1 * self.wing_force * Being.time_coeff(self.last_flap) + external_force

        # Leapfrog integration
        prev_acceleration = self.acceleration
        self.acceleration = self.force / self.mass
        self.position += self.velocity * dt + .5 * prev_acceleration * dt ** 2
        self.velocity += .5 * (self.acceleration + prev_acceleration) * dt

        self.last_flap += dt

    def draw(self, canvas: Canvas):
        if canvas.render_offset.taxicab(self.position) > canvas.max: return

        dx, dy = tuple(canvas.global_offset)
        canvas.create_rectangle(self.position.x - .5 * self.size.x + dx,
                                self.position.y - .5 * self.size.y + dy,
                                self.position.x + .5 * self.size.x + dx,
                                self.position.y + .5 * self.size.y + dy,
                                fill = '#446711')

