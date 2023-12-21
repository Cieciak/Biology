from dataclasses import dataclass
import yaml

from pprint import pprint
from .bases import NitrogenBase
from .amino import AminoAcid

@dataclass
class Profile:
    name: str
    

    @classmethod
    def fromFile(cls, path: str):
        
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
        pairing = {}

        for a, b in config['pairings']:
            pairing[a] = b
            pairing[b] = a