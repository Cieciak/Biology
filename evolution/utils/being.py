from math import exp
from .math import Vector
from .mendel import Organism, Compiler
from random import randrange

class Being:

    # The force function
    @staticmethod
    def time_coeff(t: float):
        return exp(-(4*t -2)**2)

    @classmethod
    def fromOrganism(cls, organism: Organism, position: Vector = Vector(0, 0)):
            # Map bio relay to 
            property_map = {4: ('mass', 'scal'), 
                            5: ('size', 'scal'),
                            6: ('vertical_force', 'scal'),
                            7: ('red', 'add'),
                            8: ('green', 'add'),
                            9: ('blue', 'add')}

            args = {'position': position,
                    'base_organism': organism,
                    'mass': 1.0,
                    'vertical_force': Vector(0, -200),
                    'size': Vector(20, 20),
                    'red': 0,
                    'green': 0,
                    'blue': 0,}

            compiler = Compiler()
            compiler.run(organism.get_executable())

            for key, val in property_map.items():
                name, _type = val
                if _type == 'scal': args[name] *= 1.2 ** compiler.bio_relay.get(key, 0)
                elif _type == 'add': args[name] += compiler.bio_relay.get(key, 0)

            return cls(**args)

    def __init__(self, position: Vector, base_organism: Organism, mass: float = 1.0, vertical_force: Vector = Vector(-200, 0), size = Vector(20, 20), **other) -> None:
        self.position: Vector = position         # [m]
        self.velocity: Vector = Vector(0, 0)     # [m/s]
        self.acceleration: Vector = Vector(0, 0) # [m/s^2]
        self.force: Vector = Vector(0, 0)        # [N]

        self.vertical_force: Vector  = vertical_force
        self.horizontal_force: Vector = Vector(40, 0)
        self.since_flap: float = 1e10
        self.force_dir: int = 0

        self.mass: float = mass
        self.base_organism = base_organism
        self.size: Vector = size
        self.other = other

    def __repr__(self) -> str:
        return f'{self.base_organism}'
    # Breed with the other
    def __matmul__(P1, P2):

        F1 = P1.base_organism @ P2.base_organism

        children = []
        for f in F1:
            children.append(Being.fromOrganism(f, Vector(randrange(-10, 10), randrange(-10, 10))))
        return children

    # Make JSON 
    def to_dict(self):
        return {
            'type'    : 'Being',
            'position': {'x': self.position.x, 'y': self.position.y},
            'size'    : {'x': self.size.x    , 'y': self.size.y},
            'other'   : self.other
        }

    def make_decision(self, ctx: None, dt: float):
        dist = [(self.position - poi.position) for poi in ctx.objects if type(poi) == PointOfInterest]
        dist.sort(key = abs)
        
        dir = dist[0]

        A = 1
        B = 1

        L = Vector(-0.707, -0.707).dot(dir)
        U = Vector( 0.000, -1.000).dot(dir)
        R = Vector( 0.707, -0.707).dot(dir)

        if   L == max(L, U, R):
            self.force_dir =  1
        elif U == max(L, U, R):
            self.force_dir =  0
        elif R == max(L, U, R):
            self.force_dir = -1

        if (A * dir.y + B * self.velocity.y) > 0 and self.since_flap > 1:
            self.since_flap = 0

    def update(self, ctx: None, dt: float):
        global_force = ctx.global_force

        self.make_decision(ctx, dt)

        self.force = self.vertical_force * Being.time_coeff(self.since_flap) + self.horizontal_force * self.force_dir + global_force

        prev_acceleration = self.acceleration
        self.acceleration = self.force / self.mass
        self.position += self.velocity * dt + .5 * prev_acceleration * dt ** 2
        self.velocity += .5 *(self.acceleration + prev_acceleration) * dt

        self.since_flap += dt

class PointOfInterest:

    def __init__(self, position: Vector, size: Vector, color: str, id) -> None:
        self.position = position
        self.size = size
        self.color = color
        self.id = id

    def to_dict(self):
        return {
            'type'    : 'PointOfInterest',
            'position': {'x': self.position.x, 'y': self.position.y},
            'size'    : {'x': self.size.x, 'y': self.size.y},
            'color'   : self.color
        }

    def update(self, *args, **kwargs):
        pass