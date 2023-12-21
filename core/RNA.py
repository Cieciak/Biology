from dataclasses import dataclass

from .bases import NitrogenBase
from .DNA import DNA

@dataclass
class TranscriptionRules:
    bases: list[NitrogenBase]
    pairings: dict[str, str]

    @classmethod
    def real(cls):
        bases = [
            NitrogenBase('C', 'Cyt', 'Cytozyna'),
            NitrogenBase('G', 'Gua', 'Guanina'),
            NitrogenBase('A', 'Ade', 'Adenina'),
            NitrogenBase('U', 'Ura', 'Uracyl'),
        ]
        pairing = {
            'A': 'U',
            'C': 'G',
            'G': 'C',
            'T': 'A',
        }

        return cls(bases, pairing)

class RNA:

    def __init__(self, dna: DNA, rules: TranscriptionRules):
        
        self.rules = rules

        sequence = ''
        for letter in dna.complementary:
            sequence += self.rules.pairings[letter]

        self.sequence = sequence

    def __repr__(self):
        return f'mRNA:                 {self.sequence}'