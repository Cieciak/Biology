from typing import Self
import csv, pprint, yaml

CODONS_PATH: str = './evolution/mcodons.csv'
CODONS_DICT: dict[str, str] = {}

GENE_LIB_PATH: str = './evolution/genes_lib.yaml'
GENE_LIB: dict[str, list[str]] = {}

# Read condons from file
with open(CODONS_PATH) as file:
    raw = csv.reader(file)
    for row in raw:
        # Skip empty rows
        if not row: continue

        # Get codon and amino
        codon, value = (value.strip() for value in row)
        CODONS_DICT[codon] = value

# Read genes
with open(GENE_LIB_PATH) as file:
    GENE_LIB = yaml.safe_load(file)

# Get codons by aminos
def get_codon(name: str):
    output = []
    for key, val in CODONS_DICT.items():
        if val == name: output += [key, ]
    return output

def get_DNA(name: str, domination_type: int, V1: int = 0, V2: int = 0):
    T2 = 'DOMINANT' if domination_type  % 2 else 'SUBMISSIVE'
    T1 = 'DOMINANT' if domination_type // 2 else 'SUBMISSIVE'
    
    return GENE_LIB[name][T1][V1] + GENE_LIB[name][T2][V2]


class Allele:

    def __init__(self, codons: list[str], *, name: str = '0') -> None:
        DOMINANT = get_codon('DOM')

        self.name = name
        self.codons = codons
        self.dominant = self.codons[1] in DOMINANT

    def __str__(self): return f'A{self.name}' if self.dominant else f'a{self.name}'

    def __repr__(self): return f'A{self.name}' if self.dominant else f'a{self.name}'

    def __eq__(self, other: Self): return self.codons == other.codons

    def __ne__(self, other: Self): return self.codons != other.codons

    def recombine(self): return ''.join(self.codons)

class Gene:

    @classmethod
    def make(cls, name: str, domination_type: int, V1: int = 0, V2: int = 0):
        return cls(get_DNA(name, domination_type, V1, V2), name = name, allele_name = (str(V1), str(V2)))

    @classmethod
    def zip(cls, A1: Allele, A2: Allele, *, I = '', name: str = 'G'):
        genome = f'{A1.recombine()}{I}{A2.recombine()}'
        return cls(genome, name = name, allele_name = (A1.name, A2.name))

    def __init__(self, genome: str, *, name: str = 'G', allele_name: tuple[str] = ('0', '0')) -> None:
        self.A1: Allele | None = None
        self.A2: Allele | None = None

        self.name: str = name
        self.allele_name = allele_name

        self.genome = genome

    def __repr__(self) -> str: return f'{self.name}[ {self.A1},{self.A2} ]'

    # Return selected allel from gene
    def allel(self, n: int): return self.A1 if n else self.A2

    # Return codons to execute
    def get_executable(self):
        output = []
        # If first allele is dominant put it as executable
        if self.A1.dominant: output += self.A1.codons
        # If the second is dominant and is different than the first put it as executable
        if self.A2.dominant and self.A1 != self.A2: output += self.A2.codons
        # If none are dominant put one as executable
        if not (self.A1.dominant or self.A2.dominant): output += self.A1.codons
        return output

    @property
    def genome(self): return self.__genome
    
    @genome.setter
    def genome(self, gen: str):
        START = get_codon('START')
        STOP = get_codon('STOP')
        ANAMES = list(self.allele_name)

        self.__genome = gen
        stack: list[str] = []
        alleles = []
        gather: bool = False
        while gen:
            codon = gen[:3]
            gen = gen[3:]

            # Start gathering codons
            if codon in START:
                gather = True
                stack += [codon, ]
            # Stop gathering codons and add allele
            elif codon in STOP:
                gather = False
                stack += [codon, ]
                alleles += [Allele(stack, name = ANAMES.pop(0)), ]
                stack = []
            # Add codon to stack
            elif gather:
                stack += [codon, ]
            
        self.A1, self.A2, *_ = alleles

class Organism:

    @classmethod
    def zip(cls, H1: list[Allele], H2: list[Allele], kernel: dict[int, int], *, name = None):
        genes = []
        for A1, A2 in zip(H1, H2):
            genes += [Gene.zip(A1, A2, name = name.pop(0)), ]

        return cls.fromGenes(genes, kernel = kernel)

    @classmethod
    def fromGenes(cls, genes: list[Gene], kernel: dict[int, int], *, intrones = None):
        genome = {}
        for key, val in kernel.items():
            level = genes[:val]
            genes = genes[val:]
            genome[key] = level
        
        return cls(genome, intrones = intrones)

    @classmethod
    def fromDNA(cls, DNA: str, kernel: dict[int, int]):
        START = get_codon('START')
        STOP = get_codon('STOP')

        I = []
        E = []
        gathered = ''
        count = 0
        while DNA:
            codon = DNA[:3]
            DNA = DNA[3:]

            if codon in START:
                if count == 0:
                    I.append(gathered)
                    gathered = ''
                count += 1
                gathered += codon
            elif codon in STOP and count == 2:
                gathered += codon
                E.append(gathered)
                gathered = ''
                count = 0
            else:
                gathered += codon

        genes = [Gene(ekson) for ekson in E]

        return Organism.fromGenes(genes, kernel, intrones = I)

    # Select alleles from genes
    @staticmethod
    def mask(genes: list[Gene], mask: int):
        stack = []
        for gen in genes:
            mask, flag = divmod(mask, 2)
            stack += [gen.allel(flag), ]
        return stack

    def __init__(self, genes: dict[int, list[Gene]], *, intrones: list[str] = None) -> None:
        self.genome = genes
        if not intrones: self.intrones = []
        else: self.intrones = intrones

    def __repr__(self) -> str: return ';'.join([str(gen) for gen in self.flatten()])

    def __matmul__(P1, P2: Self):
        output = []

        F1 = P1.get_haploid()
        F2 = P2.get_haploid()

        K1 = P1.get_kenel()
        N = [gen.name for gen in P1.flatten()]

        for H1 in F1:
            for H2 in F2:
                output += [Organism.zip(H1, H2, K1, name = N[::1]), ]

        return output

    # Return kernel allowing to reconstruct from flattened genome
    def get_kenel(self):
        kernel = {}
        for key, val in self.genome.items(): kernel[key] = len(val)
        return kernel

    # Flatten the genome
    def flatten(self) -> list[Gene]:
        keys = list(self.genome.keys())
        keys.sort()

        output: list[Gene] = []
        for key in keys:
            output += self.genome[key]
        return output
    
    # Return all possible haploidal options of parent
    def get_haploid(self):
        output: list[Allele] = []
        
        flatten = self.flatten()
        combinations = 2 ** len(flatten)

        for option in range(combinations):
            haploid = Organism.mask(flatten, option)
            output += [haploid, ]
        return output

    def get_DNA(self):
        genome = ''
        for I, E in zip(self.intrones, self.flatten()):
            genome += f'{I}{E.genome}'
        return genome

    def get_executable(self):
        output = []
        for gene in self.flatten():
            output += gene.get_executable()
        return [CODONS_DICT[codon] for codon in output]

class Compiler:

    def get_number(self, stream):
        number = 0
        while True:
            key = stream.pop(0)
            match key:

                case 'ADD':
                    number += 1
                case 'MUL':
                    number *= 2
                case 'SPC':
                    return number

    def get_functor(self, stream):
        s = []
        while True:
            key = stream.pop(0)
            s.append(key)
            if key == 'STOP': return s

    def __init__(self) -> None:
        self.bio_relay: dict[int, int] = {}
        self.functors: dict[int, list[str]] = {}

    def run(self, code: list[str]):
        skip: bool = False
        while code:
            key = code.pop(0)

            match key:

                case 'INC':
                    relay_id = self.get_number(code)
                    if not skip: self.bio_relay[relay_id] = self.bio_relay.get(relay_id, 0) + 1
                    skip = False
                case 'DEC':
                    relay_id = self.get_number(code)
                    if not skip: self.bio_relay[relay_id] = self.bio_relay.get(relay_id, 0) - 1
                    skip = False
                case 'NUL':
                    relay_id = self.get_number(code)
                    if not skip: self.bio_relay[relay_id] = 0
                    skip = False
                case 'CHK':
                    value = self.get_number(code)
                    if value > 0 and not skip: skip = True
                    else: skip = False
                case 'NOP':
                    skip = False
                case 'FNC':
                    functor = self.get_number(code)
                    body = self.get_functor(code)

                    if not skip: self.functors[functor] = body
                    skip = False
                case 'ACT':
                    functor = self.get_number(code)
                    if not skip: self.run(self.functors[functor])
                    skip = False

if __name__ == '__main__':
    
    GEN1 = get_DNA('INC_4', 0)
    GEN2 = get_DNA('DEC_5', 0)
    print(f'G1: {GEN1}{GEN2}')


    O1 = Organism.fromDNA(GEN1 + GEN2, {0: 1, 1: 1})

    C1 = Compiler()
    E1 = O1.get_executable()
    print(E1)
    C1.run(E1)

    print(C1.bio_relay)

    print(O1)