from dataclasses import dataclass
import yaml

from .bases import NitrogenBase
from .amino import AminoAcid

@dataclass
class Profile:
    name: str
    length: int
    overwrite: bool
    table: str
    bases: list[NitrogenBase]
    amino: list[AminoAcid]
    pairings: dict[str, str]
    

    @classmethod
    def fromFile(cls, path: str):
        '''Read profile from `.yaml` file'''
        
        # Get YAML data from the file
        with open(path, 'r') as file:
            data = yaml.safe_load(file)

        # Get current profile
        name = data['current']
        config = data[name]

        overwrite = config['overwrite']
        length = config['length']
        table = config['table']
        bases = [NitrogenBase(*args) for args in config['bases']]
        amino = [AminoAcid(*args) for args in config['amino-acids']]
        
        pairings = {}
        for a, b in config['pairings']:
            pairings[a] = b
            pairings[b] = a

        kwargs = {
            'overwrite': overwrite,
            'pairings':  pairings,
            'length':    length,
            'table':     table,
            'bases':     bases,
            'amino':     amino,
            'name':      name,
        }

        return cls(**kwargs)