from dataclasses import dataclass

from .bases import NitrogenBase

@dataclass
class SequenceRules:
    bases: list[NitrogenBase]
    pairings: dict[str, str]
    length: int

    @classmethod
    def real(cls):
        bases = [
            NitrogenBase('C', 'Cyt', 'Cytozyna'),
            NitrogenBase('G', 'Gua', 'Guanina'),
            NitrogenBase('A', 'Ade', 'Adenina'),
            NitrogenBase('T', 'Thy', 'Tymina'),
        ]
        pairings = {
            'A': 'T',
            'C': 'G',
            'G': 'C',
            'T': 'A',
        }
        length = 3

        return cls(bases, pairings, length)

class DNA:
    
    def __init__(self, sequence: str, rules: SequenceRules):

        self.rules = rules

        # Make sure all letters are upper case
        sequence = sequence.upper()
        result = self.validate(sequence)

        if result == False: raise ValueError(f'The sequence {sequence} is incorrect!')
        self.sequence = sequence

    def __repr__(self) -> str:
        return f'Coding strand:        {self.sequence}\nComplementary strand: {self.complementary}'

    def validate(self, sequence: str) -> bool:
        '''Check sequence'''

        # Check if sequence is correct length
        if len(sequence) % self.rules.length: return False

        # Find all unknown letters in sequence
        for base in self.rules.bases:
            sequence = sequence.replace(base.symbol, '')
        if sequence: return False

        return True

    @property
    def complementary(self):
        result = ''

        for letter in self.sequence:
            result += self.rules.pairings[letter]

        return result