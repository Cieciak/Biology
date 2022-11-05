from collections import namedtuple

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

        self.sequence = sequence
        self.complementary = DNA.create_complementary(sequence)

    def __repr__(self) -> str:
        return f'{self.sequence}\n{self.complementary}'

if __name__ == '__main__':
    dna = DNA('CTTGCGACGTTG')

    print(dna)