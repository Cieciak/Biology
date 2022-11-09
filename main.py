from collections import namedtuple
import csv

ChargaffRule = namedtuple('Chargaff', ['name', 'complementary'])

class DNA:

    NITROGEN_BASES = {
        'T': ChargaffRule('Thy', 'A'),
        'A': ChargaffRule('Ade', 'T'),
        'G': ChargaffRule('Gua', 'C'),
        'C': ChargaffRule('Cyt', 'G'),
    }

    # To refactor later
    @staticmethod
    def validate_sequence(genetic_sequence: str) -> str:
        '''Returns all symbols that do not match with nitrogen bases in DNA'''
        if len(genetic_sequence) % 3 != 0: raise ValueError('Length of given DNA sequence is not a multiple of 3')
        processed_sequence = genetic_sequence[::]
        for base in DNA.NITROGEN_BASES.keys():
            processed_sequence = processed_sequence.replace(base, '')
        return processed_sequence

    # To refactor later (dict map)
    @staticmethod
    def create_complementary(sequence: str) -> str:
        '''Returns complementary sequence of nitrogen bases'''
        complementary_sequence = ''
        for base in sequence:
            complementary_sequence += DNA.NITROGEN_BASES[base].complementary
        return complementary_sequence

    def __init__(self, sequence: str) -> None:
        sequence = sequence.upper()
        residue = DNA.validate_sequence(sequence)
        if residue:
            unknown = list(residue) if len(residue) < 4 else '[' + ' ,'.join(residue[0:2]) + f' ... ,{residue[-1]}]'
            raise ValueError(f'Found unknown nitrogen bases {unknown} in given DNA sequence')

        self.coding_strand = sequence
        self.template_strand = DNA.create_complementary(sequence)

    def __repr__(self) -> str:
        return f'{self.coding_strand}\n{self.template_strand}'

class RNA:

    NITROGEN_BASES = {
        'A': 'U',
        'C': 'G',
        'G': 'C',
        'T': 'A',
    }

        # To refactor later (dict map)
    @staticmethod
    def create_complementary(sequence: str) -> str:
        '''Returns complementary sequence of nitrogen bases'''
        complementary_sequence = ''
        for base in sequence:
            complementary_sequence += RNA.NITROGEN_BASES[base]
        return complementary_sequence

    def __init__(self, dna: DNA) -> None:
        sequence = dna.template_strand
        self.trasported_strand: str = RNA.create_complementary(sequence)

    def __repr__(self) -> str:
        return self.trasported_strand

class Compiler:

    def __init__(self, path: str):

        self.genetic_code: dict[str, str] = {}
        with open(path, 'r') as file:
            genetic_code = csv.reader(file)

            for row in genetic_code:
                if row: self.genetic_code[row[0]] = row[1].strip()

    def compile(self, rna: RNA):
        rest = rna.trasported_strand
        aminoacid = []
        while rest:
            codon = rest[:3]
            rest = rest[3:]

            aminoacid.append(self.genetic_code[codon].capitalize())

        return '-'.join(aminoacid)


if __name__ == '__main__':
    dna = DNA('CTTGCGACGTTG')

    rna = RNA(dna)

    cmp = Compiler('./codons.csv')

    print(dna)

    print(rna)

    print(cmp.compile(rna))