import csv, random

CODONS_PATH: str = './csv/mcodons.csv'
CODONS_DICT: dict[str, str] = {}

# Read codons from csv
with open(CODONS_PATH, 'r') as file:
    raw = csv.reader(file)
    for row in raw:
        if row:
            row = [x.strip() for x in row]
            codon, value = row
            CODONS_DICT[codon] = value

class Allele:

    def __init__(self, sequence: str, recesive: bool, *, name: str = 'allel'):
        self.sequence = sequence
        self.recesive = recesive
        self.name = name

    def __str__(self) -> str:
        # If asked for string return genetic sequence
        return self.sequence.lower() if self.recesive else self.sequence.upper()

    def __repr__(self) -> str:
        # If asked for representation return long description
        return ('Recesive ' if self.recesive else 'Dominative ') + f'allel: {self.sequence}'
    
    def letter(self) -> str:
        return 'Aa'[self.recesive]

class Gen:

    @classmethod
    def fromDNA(cls, genetic_sequences: list[str], mask: list[bool]):
        # Given DNA snippets and mask create gen
        alleles: list[Allele] = []
        for allel, flag in zip(genetic_sequences, mask):
            alleles.append(Allele(allel, flag))

        return cls(alleles)

    def __init__(self, alleles: list[Allele], *, name: str = 'gen'):
        # All of the copies of gene
        self.alleles = alleles
        # Dominant copies of gene
        self.dominant = [version for version in alleles if not version.recesive]

        self.name = name

    def __repr__(self) -> str: 
        return ('Dominant ' if self.dominant else 'Recesive ') + self.name


class Organism:

    @classmethod
    def fromDNA(cls, dna: str, codons: dict[str , str]):
        
        dna = dna.replace(' ', '')

        # Find the STOP and DOM codon
        STOP = Organism.find_codon(codons, 'STOP')
        DOM =  Organism.find_codon(codons, 'DOM')

        # Split genome at every STOP codon
        gene = ''
        genes = []
        while dna:
            codon = dna[:3]
            dna = dna[3:]
            if codon == STOP:
                genes.append(gene)
                gene = ''
                continue
            gene += codon

        # Scan code for genes
        genome = []
        while genes:
            gen = genes[:2]
            mask = [False if allel.startswith(DOM) else True for allel in gen]
            # Make the gene
            if not gen: break
            genome.append(Gen.fromDNA(gen, mask))
            genes = genes[2:]
        return cls(genome, codons)

    @staticmethod
    def find_codon(codons: dict[str, str], token: str):
        for key, codon in codons.items():
            if codon == token: return key

    @staticmethod
    def mask(genotyp: list[Gen], mask: int) -> list[Allele]:
        # Iterate genes and select 0th or 1st version based on mask
        output: list[Allele] = []
        for gene in genotyp:
            mask, flag = divmod(mask, 2)
            output.append(gene.alleles[flag])

        return output

    def __init__(self, genes: list[Gen], codons: dict[str, str] = CODONS_DICT):
        
        self.genes = genes
        self.codons = codons

    def __repr__(self) -> str:
        output: list[str] = []
        for index, gen in enumerate(self.genes):
            gene_name = f'G{index}' if gen.dominant else f'g{index}'
            name = gene_name + f'[{"".join(allel.letter() for allel in gen.alleles)}]'
            output.append(name)
        return ', '.join(output)

    def __matmul__(parent_one, parent_two):
        # Return all combinations
        output: list[Organism] = []

        # Get haploidal options of parents
        P1_HALF = parent_one.get_haploid()
        P2_HALF = parent_two.get_haploid()

        # For each option of first parent
        for P1_OPT in P1_HALF:
            # Iterate over every option of the second parent
            for P2_OPT in P2_HALF:
                # Match the genes
                genom = []
                # And make new organism using collected genes
                for P1_ALLEL, P2_ALLEL in zip(P1_OPT, P2_OPT): genom.append(Gen([P1_ALLEL,P2_ALLEL]))
                output.append(Organism(genom))
        return output

    def get_haploid(self):
        # Return all haploidal options of parent
        output: list = []
        combinations: int = 2 ** len(self.genes)

        for option in range(combinations):
            haploid = tuple(Organism.mask(self.genes, option))
            output.append(haploid)

        return output

    def executable_dna(self, translate: bool = True):
        output = []
        for gen in self.genes:
            sequence = random.choice(gen.dominant).sequence if gen.dominant else random.choice(gen.alleles).sequence
            gen_codons = []
            while sequence:
                codon = sequence[:3]
                sequence = sequence[3:]
                gen_codons.append(self.codons[codon] if translate else codon)
            output.append(gen_codons)

        return output

    def dump_dna(self):
        output = ''
        o = []
        for gen in self.genes:
            o.extend([a.sequence for a in gen.alleles])
        output = 'G'.join(o) + 'G'
        return output
    
if __name__ == '__main__':

    org1 = Organism.fromDNA('CCG CAT CCT TTT TAA TTT CCG GAG CCT CTC TTT CCG GAG CCT CTC TTT CAT CTC CTC CTC TTT CAT CTC CTC CTC TTT', CODONS_DICT)
    org2 = Organism.fromDNA('TAA         TTT TAA TTT CAT CTC CTC     TTT CAT CCT CTT     TTT GAG CTC CTC CTC TTT GAG CTC CTC CTC TTT', CODONS_DICT)
    print('Organism one:', org1)
    print('Organism two:', org2)

    print('Children:', random.choice(org1 @ org2).executable_dna())
