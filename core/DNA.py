from .profile import Profile

import random

class DNA:

    @classmethod
    def random(cls, profile: Profile, *, lenght = 10):
        '''Generate random DNA strand. `length` specifies number of CODONS'''

        START = random.choice(profile.special['start'])
        STOP  = random.choice(profile.special['stop'])

        START = random.choice(profile.codon(START))
        STOP  = random.choice(profile.codon(STOP))

        bases = random.choices(profile.bases, k = lenght * profile.length)
        sequence = ''.join(base.symbol for base in bases)

        return cls(f'{START}{sequence}{STOP}', profile)

    @classmethod
    def fromAmino(cls, protein: list[str], profile: Profile):

        sequence: str = ''
        for amino in protein:
            codons = profile.codon(amino)

            sequence += random.choice(codons)

        return cls(sequence, profile)

    def __init__(self, sequence: str, profile: Profile):

        self.profile = profile

        # Sanitize the input data
        sequence = sequence.upper()
        self.validate(sequence)

        self.coding_strand = sequence

    def __repr__(self) -> str:
        return f'Coding strand: {self.coding_strand}'

    def __getitem__(self, index) -> str:

        start = self.profile.length *  index
        stop  = self.profile.length * (index + 1)

        return self.coding_strand[start:stop]

    def validate(self, sequence: str):

        # Check if lenght is correct
        if len(sequence) % self.profile.length: raise ValueError(f'Sequence of lenght {len(sequence)} cannot be used in profile of lenght {self.profile.length}')

        # Chek for unknown characters in the strand
        for base in self.profile.bases:
            sequence = sequence.replace(base.symbol, '')
        if sequence: raise ValueError(f'Found unknown characters in sequence. \"{sequence}\"')

    def test(self, marker: str, n: int = 0) -> bool:
        '''Test if `n`th codon is of given special type'''
        abbr  = [it.abbr for it in self.profile.special.get(marker, [])]
        codon = self[n]
        return  self.profile.codons[codon] in abbr
    
    @property
    def info(self) -> dict:
        data = {
            'strand': self.coding_strand,
            'dominant': self.dominant,
            'lenght': len(self.coding_strand),
        }

        return data

    @property
    def dominant(self) -> bool:
        return self.test('dominant', n = 1)