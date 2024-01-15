from .organism import Organism

class Builder:

    def __init__(self):
        ...

    def fromOrganism(organism: Organism):
        sequence = organism.executable()
        amino    = []

        while sequence:
            codon    = sequence[:3]
            sequence = sequence[3:]

            amino += [organism.profile.codons[codon]]

        return amino
    
    def fromDna(dna):
        sequence = dna.coding_strand
        amino    = []

        while sequence:
            codon    = sequence[:3]
            sequence = sequence[3:]

            amino += [dna.profile.codons[codon]]

        return amino


class Compiler:

    def __init__(self):

        self.stack: list = []

        self.action: {}

    def make(self, protein: list[str]):

        self.digit = 0
        self.result = {}

        for token in protein:
            self.action[token](self)

        print(self.stack)
        return self.result

def zer_action(c: Compiler):
    c.digit *= 2

def one_action(c: Compiler):
    c.digit *= 2
    c.digit += 1

def key_action(c):
    c.stack.append(c.digit)
    c.digit = 0
    c.stack.append('key')

def val_action(c):
    c.stack.append(c.digit)
    print(f'Val {c.stack}, {c.digit}')
    c.digit = 0
    c.stack.append('val')

A = {
    'START': lambda x: None,
    'STOP': lambda x: None,
    'KEY': key_action,
    'VAL': val_action,
    'DOM': lambda c: None,
    'ZER': zer_action,
    'ONE': one_action,
}



class Being:

    def __init__(self):
        self.properties = {}