import core
import tools
import random

from pprint import pprint

if __name__ == '__main__':
    profile = core.getProfile('./profiles.yaml')

    A1 = core.DNA.fromAmino(tools.getGene('./code/test.gen'), profile)
    A2 = core.DNA.fromAmino(['START', 'ZER', 'KEY', 'ZER', 'VAL', 'STOP'], profile)

    D2 = core.DNA.fromAmino(['START', 'DOM', 'ZER', 'KEY', 'ONE', 'ONE', 'VAL', 'STOP'], profile)

    G1 = core.Gene(A1, A2, profile)

    G2 = core.Gene(D2, D2, profile)

    O1 = core.Organism([G1], kernel = [1], profile = profile)

    O2 = O1 @ O1

    pprint(O1.info)

    print(O1.executable)

    print(O1.haploid())

    pprint(O2)

    c = core.Creator(profile, core.A)
    for o in O2:
        P = c.make(o.executable)
        print(P)

    r = tools.Reader()

    data = tools.getGene('./code/test.gen')

    print(data)