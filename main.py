import biology.core as core

from pprint import pprint

if __name__ == '__main__':

    profile = core.getProfile('./profiles.yaml')

    G1 = core.getGene('./code/SET_ZERO.gen', profile)
    G2 = core.getGene('./code/SET_ONE.gen', profile)

    O1 = core.Organism([G1, G2], kernel = [2], profile = profile)

    O2 = O1 @ O1

    pprint(O1.info)

    print(O1.executable)

    pprint(O1.haploid())

    pprint(O2)

    c = core.Creator(profile, core.A)
    for o in O2:
        P = c.make(o.executable)
        print(P)