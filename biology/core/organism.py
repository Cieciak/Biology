from typing import Self

from .genetics.gene import Gene
from .profile import Profile
from .genetics.DNA import DNA

class Organism:

    @classmethod
    def random(cls, profile: Profile):
        G1 = Gene.random(profile)
        G2 = Gene.random(profile)

        return cls([G1, G2], profile)

    def __init__(self, genome: list[Gene] = None, kernel: list[int] = None, profile: Profile = None):
        
        if not genome: raise ValueError('Cannot create organism without genes')
        if not kernel: raise ValueError('Cannot create organism without kernel')
        
        self.genome: list[list[Gene]] = []
        for size in kernel:
            layer = []

            for index in range(size):
                layer += [genome.pop(0)]

            self.genome.append(layer)


        self.kernel: list[int]  = kernel
        self.profile: Profile   = profile

    def __repr__(self) -> str:
        
        lines: list[str] = []
        for index, gene in enumerate(self.flatten):
            lines += [f'G{index}[{gene}]']

        return ', '.join(lines)

    def __matmul__(P1, P2: Self) -> list[Self]:

        F1 = P1.haploid()
        F2 = P2.haploid()

        K  = P1.kernel
        P  = P1.profile

        children: list[Self] = []
        for H1 in F1:
            for H2 in F2:
                genome = [Gene(A1, A2, P) for A1, A2 in zip(H1, H2)]

                children.append(Organism(genome, K, P))

        return children

    def haploid(self) -> list[list[DNA]]:
        output: list[list[DNA]] = []

        combinations = 2 ** len(self.flatten)

        for option in range(combinations):
            haploid = Organism.mask(self.flatten, option)

            output += [haploid]

        return output

    @staticmethod
    def mask(genes: list[Gene], mask: int) -> list[DNA]:

        allele: list[DNA] = []

        for gen in genes:
            mask, flag = divmod(mask, 2)

            allele += [gen.A(flag)]

        return allele

    @property
    def flatten(self) -> list[Gene]:
        genes: list[Gene] = []
        for layer in self.genome: genes += layer

        return genes

    @property
    def info(self) -> dict:
        return {
            'kernel': self.kernel,
            'genome': self.genome,
        }
    
    @property
    def executable(self):
        '''Executable DNA of this organism'''
        genes: list[Gene] = []
        for layer in self.genome: genes += layer
        
        strands: list[DNA] = [gen.executable() for gen in genes]
        return ''.join(strands)