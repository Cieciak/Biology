from dataclasses import dataclass
import random, csv

from .amino import AminoAcid
from .bases import NitrogenBase
from .profile import Profile

############################################
##
## This may be integrated into Profile class
##
############################################

class CodonCreator:

    def __init__(self, profile: Profile):
        self.profile = profile

        self.CODON_LENGTH: int            = profile.length
        self.BASES: list[NitrogenBase]    = profile.bases
        self.AMINO_ACIDS: list[AminoAcid] = profile.amino

    @staticmethod
    def convertNumber(n: int, base: int) -> list[int]:
        '''Convert `n` to list of digits'''
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
    
    def assignAminoAcids(self, codons: list[str] = None) -> dict[str, str]:
        '''Assign amino acids to codons'''
        self.pairs: dict[str, str] = {}

        codons = codons or self.codons

        for codon in codons:
            amino = random.choice(self.AMINO_ACIDS)
            
            self.pairs[codon] = amino.abbr

        return self.pairs

    def generate(self) -> dict[str, str]:
        self.creatateAllCodons()
        data = self.assignAminoAcids()

        return data

    def dumpCSV(self, path: str = None):
        '''Dump generated pairs to `.csv` file'''
        if self.profile.overwrite == False: raise PermissionError('The file is set as read only')

        path = path or self.profile.table

        with open(path, 'w') as file:
            CSV = csv.writer(file)

            for base, amino in self.pairs.items():
                CSV.writerow((base, amino))

    def getTable(self, path: str = None) -> dict[str, str]:
        '''Get `codon` to `amino-acid` table'''
        if self.pairs: return self.pairs

        path = path or self.profile.table

        pairs: dict[str, str] = {}
        with open(path, 'r') as file:
            CSV = csv.reader(file)

            for codon, amino in CSV:
                pairs[codon] = amino

        return pairs
    
    def updateProfile(self) -> Profile:
        '''Update profile with current codon table'''

        self.profile.codons = self.getTable(self.profile.table)

        return self.profile
    
def getProfile(path: str) -> Profile:

    base = Profile.fromFile(path)

    creator = CodonCreator(base)

    creator.generate()
    creator.dumpCSV()

    profile = creator.updateProfile()

    return profile