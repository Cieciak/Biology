import core
import random

from pprint import pprint

if __name__ == '__main__':
    profile = core.getProfile('./profiles.yaml')

    dna = core.DNA.fromAmino(['START', 'DOM', 'KEY', 'ZER', 'VAL', 'ONE', 'STOP'], profile)

    protein = core.Builder.fromDna(dna)

    pprint(dna.info)
    print(protein)

    c = core.Compiler()
    c.action = core.A

    d = c.make(protein)

    print(d)