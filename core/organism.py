from .gene import Gene
from .profile import Profile
from .DNA import DNA

class Organism:

    @classmethod
    def random(cls, profile: Profile):
        G1 = Gene.random(profile)
        G2 = Gene.random(profile)

        return cls([G1, G2], profile)

    def __init__(self, genome: list[Gene] = None, kernel: list[int] = None, profile: Profile = None):
        
        if not genome: raise ValueError('Cannot create organism without genes')
        if not kernel: raise ValueError('Cannot create organism without kernel')
        
        self.kernel: list[int]  = kernel
        self.genome: list[Gene] = genome 

        self.profile: Profile   = profile

    def __repr__(self) -> str:
        
        lines: list[str] = []
        for index, gene in enumerate(self.genome):
            lines += [f'G{index}[{gene}]']

        return ', '.join(lines)
    
    def executable(self):
        
        strands: list[DNA] = [gen.executable() for gen in self.genome]
        return ''.join(strands)