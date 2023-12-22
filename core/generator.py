from dataclasses import dataclass
import random, csv

from .amino import AminoAcid
from .bases import NitrogenBase
from .profile import Profile

@dataclass
class Pair:
    base: str
    amino: str


class CodonCreator:

    def __init__(self, profile: Profile):
        self.profile = profile

        self.CODON_LENGTH: int            = profile.length
        self.BASES: list[NitrogenBase]    = profile.bases
        self.AMINO_ACIDS: list[AminoAcid] = profile.amino

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
            
            self.pairs += [Pair(codon, amino.abbr)]

        return self.pairs

    def generate(self) -> list[Pair]:
        self.creatateAllCodons()
        data = self.assignAminoAcids()

        return data

    def dumpCSV(self, path: str = None):
        '''Dump generated pairs to `.csv` file'''
        if self.profile.overwrite == False: raise PermissionError('The file is set as read only')

        if path is None: path = self.profile.table
        with open(path, 'w') as file:
            CSV = csv.writer(file)

            for pair in self.pairs:
                CSV.writerow((pair.base, pair.amino))
