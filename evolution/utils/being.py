from math import exp
from .math import Vector
from .mendel import Organism

class Being:

    @staticmethod
    def time_coeff(t: float):
        return exp(-(4*t -2)**2)

    
    @classmethod
    def fromOrganism(cls, organism: Organism):
        executable = organism.executable_dna()
        keys = ['size', 'vertical_force', 'mass']
        defa = [Vector(20, 20), Vector(0, -200), float(1.0)]
        args = {}
        mode = ''
        counter = 0
        for gene in executable:
            for opcode in gene:
                match opcode:
                    case 'NOP': pass

                    case 'INC':
                        if counter == 0: 
                            mode = 'inc'
                        elif mode == 'inc':
                            defa[counter - 1] *= 1.2
                            counter = 0
                        elif mode == 'dec':
                            defa[counter - 1] *= 0.8
                            counter = 0
                    case 'DEC':
                        if counter == 0: 
                            mode = 'dec'
                        elif mode == 'inc':
                            defa[counter - 1] *= 1.2
                            counter = 0
                        elif mode == 'dec':
                            defa[counter - 1] *= 0.8
                            counter = 0
                    case 'ONE':
                        counter += 1
            for key, val in zip(keys, defa):
                args[key] = val

            print(args)
            return cls(Vector(0, 0), **args)

    def __init__(self, position: Vector, mass: float = 1.0, vertical_force: Vector = Vector(-200, 0), size = Vector(20, 20)) -> None:
        self.position: Vector = position         # [m]
        self.velocity: Vector = Vector(0, 0)     # [m/s]
        self.acceleration: Vector = Vector(0, 0) # [m/s^2]
        self.force: Vector = Vector(0, 0)        # [N]

        self.vertical_force: Vector  = vertical_force
        self.horizontal_force: Vector = Vector(40, 0)
        self.since_flap: float = 1e10
        self.force_dir: int = 0

        self.mass: float = mass

    def to_dict(self):
        return {'x': self.position.x, 'y': self.position.y}

    def make_decision(self, ctx: None, dt: float):
        if self.since_flap > 1:
            self.since_flap = 0

    def update(self, ctx: None, dt: float, external_force: Vector = Vector(0, 0)):
        self.make_decision(ctx, dt)

        self.force = self.vertical_force * Being.time_coeff(self.since_flap) + self.horizontal_force * self.force_dir + external_force

        prev_acceleration = self.acceleration
        self.acceleration = self.force / self.mass
        self.position += self.velocity * dt + .5 * prev_acceleration * dt ** 2
        self.velocity += .5 *(self.acceleration + prev_acceleration) * dt

        self.since_flap += dt