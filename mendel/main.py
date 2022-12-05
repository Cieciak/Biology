from pprint import pprint
from collections import namedtuple

Entry = namedtuple('Entry', ['organism', 'percent'])

def matrix(x, y):
    output = []
    for i in range(y):
        row = []
        for j in range(x):
            row.append('')
        output.append(row)
    return output

first_column = lambda text, padding:  f'{text:^{padding}}'
rest_columns = lambda list, padding: [f'{text:^{padding}}' for text in list]

row_dis = lambda first, rest: first + '|' + '|'.join(rest)

class Organism:

    @staticmethod
    def split_alleles(genes: str) -> list[str]:
        output: list[str] = []
        while genes:
            allele = genes[:2]
            genes = genes[2:]
            output.append(allele)
    
        return output

    @staticmethod
    def mask(alleles: list[str], mask: int) -> str:
        output: str = ''
        for allele in alleles:
            mask, remainder = divmod(mask, 2)
            output += allele[remainder]
        return output

    @staticmethod
    def prune(combinations: list[str]) -> list[str]:
        output: list[str] = []
        sets: list[set] = []

        for combination in combinations:
            if set(combination) not in sets: 
                output.append(combination)
                sets.append(set(combination))
        return output

    def __init__(self,genes) -> None:
        self.genes = genes

    def __repr__(self) -> str:
        return f'{self.genes}'

    def __matmul__(self, other):
        # This will return matrix of all options
        self_half = self.get_all_combinations()
        other_half = other.get_all_combinations()

        pool = matrix(len(self_half), len(other_half))

        for j, second in enumerate(other_half):
            for i, first in enumerate(self_half):
                gene = ''
                for p1, p2 in zip(first, second):
                    gene += f'{p1}{p2}' if ord(p1) < ord(p2) else f'{p2}{p1}'
                pool[i][j] = Organism(gene)

        return pool

    def get_all_combinations(self):
        output: list[str] = []

        pairs = Organism.split_alleles(self.genes)
        genes = len(pairs)
        
        for number in range(2 ** genes):
            option = Organism.mask(pairs, number)
            output.append(option)

        return output

def print_matrix(p1: Organism, p2: Organism, table: list[list[Organism]]):

    top_row = row_dis(first_column('P', 1 + len(p2.genes)), rest_columns(p2.get_all_combinations(), 1 + len(p1.genes)))
    print(top_row)
    for option, table_row in zip(p1.get_all_combinations(), table):
        row = row_dis(first_column(option, 1 + len(p2.genes)), rest_columns(map(lambda x: x.genes, table_row), 1 + len(p1.genes)))
        print(row)
    
def flatten(matrix: list[list[Organism]]):
    output = []
    for row in matrix:
        for element in row:
            output.append(element)

    return output

def minimalze(array: list[Organism]):
    output = {}
    for i in array:
        try:
            output[i.genes] += 1
        except KeyError:
            output[i.genes] = 1
    o = []
    for key, value in output.items():
        o.append(Entry(key, value / len(array)))
    o.sort(key= lambda x: x.percent, reverse=1)
    return o

if __name__ == '__main__':

    import sys

    p1 = Organism(sys.argv[1])
    p2 = Organism(sys.argv[2])

    print(f'Parent 1: {p1}')
    print(f'Parent 2: {p2}')
    print()

    f1 = p1 @ p2
    print_matrix(p1, p2, f1)
    print()
    f = flatten(f1)

    for child in minimalze(f):
        print(f'{child.organism}: {child.percent * 100}%')