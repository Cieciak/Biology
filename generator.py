from pprint import pprint
import random, csv

from dataclasses import dataclass

@dataclass
class NitrogenBase:
    symbol: str
    abbr: str
    name: str

@dataclass
class Pair:
    base: str
    amino: str

CODON_LENGTH = 3

# These are real nitrogen bases
NITROGEN_BASES = [
    NitrogenBase('T', 'Thy', 'Tymina'),
    NitrogenBase('A', 'Ade', 'Adenina'),
    NitrogenBase('C', 'Cyt', 'Cytozyna'),
    NitrogenBase('G', 'Gua', 'GUanina'),
]

# These are my made up bases
EXTENDED_NITROGEN_BASES = [
    NitrogenBase('T', 'Thy', 'Tymina'),
    NitrogenBase('A', 'Ade', 'Adenina'),
    NitrogenBase('C', 'Cyt', 'Cytozyna'),
    NitrogenBase('G', 'Gua', 'Guanina'),
    NitrogenBase('X', 'Xhy', 'Kshylinina'),
    NitrogenBase('Z', 'Zyp', 'Zyprolina'),
]

# This is totally made up
AMINO_ACIDS = [
    'START',
    'NOP',
    'NUL',
    'INC',
    'DEC',
    'SPC',
    'ADD',
    'MUL',
    'CHK',
    'FNC',
    'ACT',
    'STOP',
]

class CodonCreator:

    def __init__(self, bases: list[NitrogenBase] = NITROGEN_BASES, aminos: list[str] = AMINO_ACIDS, length: int = 3):
        self.CODON_LENGTH: int         = length
        self.BASES: list[NitrogenBase] = bases
        self.AMINO_ACIDS: list[str]    = aminos

    @staticmethod
    def convertNumber(n: int, base: int) -> list[int]:
        '''Convert n to list of digits'''
        if n == 0: return [0,]

        digits: list[int] = []
        while n:
            n, digit = divmod(n, base)
            digits += [digit, ]

        return digits

    def createCodon(self, n: list[int]) -> str:
        '''Make codon by assigning each digit in `n` a nitrogen base'''
        codon = ''

        # Make sure the length is at least the length of codon
        n += [0] * self.CODON_LENGTH

        for digit in n[:self.CODON_LENGTH]:
            codon += self.BASES[digit].symbol

        return codon

    def creatateAllCodons(self) -> list[str]:
        '''Generate list of all codons'''
        self.codons: list[str] = []

        for index in range(len(self.BASES) ** self.CODON_LENGTH):
            current = self.convertNumber(index, len(self.BASES))
            codon   = self.createCodon(current)

            self.codons += [codon]

        return self.codons
    
    def assignAminoAcids(self, codons: list[str] = None) -> list[Pair]:
        '''Assign amino acids to codons'''
        self.pairs: list[Pair] = []

        if not codons: codons = self.codons

        for codon in codons:
            amino = random.choice(self.AMINO_ACIDS)
            
            self.pairs += [Pair(codon, amino)]

        return self.pairs

    def gernerate(self) -> list[Pair]:
        self.creatateAllCodons()
        data = self.assignAminoAcids()

        return data

    def dumpCSV(self, path: str):
        '''Dump generated pairs to `.csv` file'''
        with open(path, 'w') as file:
            CSV = csv.writer(file)

            for pair in self.pairs:
                CSV.writerow((pair.base, pair.amino))


if __name__ == '__main__':
    creator = CodonCreator()

    data = creator.gernerate()
    pprint(data)