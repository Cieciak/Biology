from pprint import pprint
import random, csv

CODON_LENGTH = 3

NITROGEN_BASES = [
    ('T', 'Thy', 'Tymina'),
    ('A', 'Ade', 'Adenina'),
    ('C', 'Cyt', 'Cytozyna'),
    ('G', 'Gua', 'Guanina')
]

EXTENDED_NITROGEN_BASES = [
    ('T', 'Thy', 'Tymina'),
    ('A', 'Ade', 'Adenina'),
    ('C', 'Cyt', 'Cytozyna'),
    ('G', 'Gua', 'Guanina'),
    ('X', 'Xhy', 'Kshylinina'),
    ('Z', 'Zyp', 'Zyprolina')
]

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

def convertBase(n: int, base: int) -> list[int]:
    if n == 0: return [0,]
    digits: list[int] = []
    while n:
        n, digit = divmod(n, base)
        digits += [digit, ]
    return digits

def createCodon(n: list[int], bases: list[tuple[str, str, str]]):
    codon = ''
    n += [0] * CODON_LENGTH
    for digit in n[:CODON_LENGTH]:
        codon += bases[digit][0]
    return codon

def creatateCodons(bases: list[tuple[str, str, str]], length: int):
    codons = []
    for index in range(len(bases) ** length):
        current = convertBase(index, len(bases))
        codon = createCodon(current, bases)
        codons += [codon, ]

    return codons

def assignAminoAcids(codons: list[str], amino_acids: list[str]):
    pairs = []
    for codon in codons:
        amino = random.choice(amino_acids)
        pairs += [(codon, amino), ]
    return pairs

def dumpCSV(path: str, pairs: list[tuple[str, str]]):
    with open(path, 'w') as file:
        CSV = csv.writer(file)
        for pair in pairs:
            CSV.writerow(pair)

if __name__ == '__main__':
    CODONS = creatateCodons(NITROGEN_BASES, CODON_LENGTH)
    pprint(CODONS)

    PAIRS = assignAminoAcids(CODONS, AMINO_ACIDS)
    pprint(PAIRS)

    dumpCSV('./codons/codons.csv', PAIRS)