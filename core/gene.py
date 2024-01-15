from .DNA import DNA
from .profile import Profile

class Gene:

    @classmethod
    def random(cls, profile: Profile):
        A1 = DNA.random(profile)
        A2 = DNA.random(profile)

        return cls(A1, A2, profile)
    
    def __init__(self, A1: DNA, A2: DNA, profile: Profile):

        self.profile = profile
        self.A1: DNA = A1
        self.A2: DNA = A2

    def __repr__(self) -> str:
        return f'[A1[{self.A1}], A2[{self.A2}]]'
    
    def executable(self):
        if not (self.A1.dominant ^ self.A2.dominant): return f'{self.A1.coding_strand}{self.A2.coding_strand}'
        elif self.A1.dominant: return f'{self.A1.coding_strand}'
        elif self.A2.dominant: return f'{self.A2.coding_strand}'