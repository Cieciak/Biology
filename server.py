import biology.app.server
from biology.app.object import Being
from biology.app.math import Vector

from biology.core import getGene, getProfile, Organism, Creator, A

if __name__ == '__main__':

    PROFILE = getProfile('./profiles.yaml')
    GENOME = [
        getGene('./code/SET_ZERO.gen', PROFILE),
    ]
    KERNEL = [1]

    O1 = Organism(GENOME, KERNEL, PROFILE)
    C = Creator(PROFILE, A)

    pmap = {
        0: ('size', 'scale'),
    }

    OBJECTS = [
        Being.fromOrganism(O1, position = Vector(0, -100),pmap = pmap, creator = C),
        Being.fromOrganism(O1, position = Vector(0,  100),pmap = pmap, creator = C),
    ]

    server = biology.app.server.Server(creator = C, objects = OBJECTS)

    server.serve()