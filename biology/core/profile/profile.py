from ..genetics.bases import NitrogenBase
from ..genetics.amino import AminoAcid

from dataclasses import dataclass, field
import yaml


@dataclass
class Profile:
    name:      str
    length:    int
    overwrite: bool
    table:     str
    bases:     list[NitrogenBase]
    amino:     list[AminoAcid]
    pairings:  dict[str, str]
    codons:    dict[str, str]             = field(default_factory = dict)
    special:   dict[str, list[AminoAcid]] = field(default_factory = dict)

    @classmethod
    def fromFile(cls, path: str):
        '''Read profile from `.yaml` file'''
        
        # Get YAML data from the file
        with open(path, 'r') as file:
            data = yaml.safe_load(file)

        # Get current profile
        name = data['current']
        config = data[name]

        # Get all special codons
        special = {}
        special_amino = []
        for function, values in config['special'].items():
            amino = [AminoAcid(*args) for args in values]
            special_amino += amino
            special[function] = amino

        # Get all other stuff
        overwrite = config['overwrite']
        length = config['length']
        table = config['table']
        bases = [NitrogenBase(*args) for args in config['bases']]
        amino = [AminoAcid(*args) for args in config['amino-acids']] + special_amino
        
        # Create rules for pairing bases
        pairings = {}
        for a, b in config['pairings']:
            pairings[a] = b
            pairings[b] = a

        # Map
        kwargs = {
            'overwrite': overwrite,
            'pairings':  pairings,
            'special':   special,
            'length':    length,
            'table':     table,
            'bases':     bases,
            'amino':     amino,
            'name':      name,
        }

        return cls(**kwargs)
    
    def codon(self, amino: str) -> list[str]:

        if type(amino) == AminoAcid: amino = amino.abbr

        return [key for key, value in self.codons.items() if value == amino]