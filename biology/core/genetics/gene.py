from .DNA import DNA
from ..profile import Profile

class Gene:

    @classmethod
    def random(cls, profile: Profile):
        A1 = DNA.random(profile)
        A2 = DNA.random(profile)

        return cls(A1, A2, profile)
    
    @classmethod
    def fromAmino(cls, S1: list[str], S2: list[str], profile: Profile):
        A1 = DNA.fromAmino(S1, profile)
        A2 = DNA.fromAmino(S2, profile)

        return cls(A1, A2, profile)
    
    def __init__(self, A1: DNA, A2: DNA, profile: Profile):

        self.profile = profile
        self.A1: DNA = A1
        self.A2: DNA = A2

    def __repr__(self) -> str:

        left  = 'A' if self.A1.dominant else 'a'
        right = 'A' if self.A2.dominant else 'a'

        return f'{left}{right}'
    
    def executable(self):
        if not (self.A1.dominant ^ self.A2.dominant): return f'{self.A1.coding_strand}{self.A2.coding_strand}'
        elif self.A1.dominant: return f'{self.A1.coding_strand}'
        elif self.A2.dominant: return f'{self.A2.coding_strand}'

    def A(self, index: int) -> DNA:
        return [self.A1, self.A2][index] # Black magic fuckery, to avoid ifs, and error handling