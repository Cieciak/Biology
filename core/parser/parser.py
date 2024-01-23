from ..genetics.gene import Gene
from ..profile import Profile
import re

# Function to break string after the index
def breaks(string: str, index: int) -> (str, str):
    return string[:index], string[index:]

class Reader:

    def __init__(self):
        ...

    @staticmethod
    def consume_allel(data: str) -> (list[str], str):
        orders: list[str] = []
        skip: bool = False

        # Patterns
        segment = re.compile(r'^[\w]+')
        space   = re.compile(r'^ +')
        newline = re.compile(r'^\n')
        comment = re.compile(r'^;')
        allel   = re.compile(r'^#allel')

        while data:

            # Skip everything until newline is found
            if skip and not newline.match(data):
                void, data = breaks(data, 1)
                continue
            elif skip and newline.match(data):
                void, data = breaks(data, 1)
                skip = False
                continue

            # Find every token
            match = segment.match(data)
            if match:
                order, data = breaks(data, match.end())
                orders += [order]

                continue
            
            # Skip every space
            match = space.match(data)
            if match:
                order, data = breaks(data, match.end())

                continue

            # Skip newline too
            match = newline.match(data)
            if match:
                order, data = breaks(data, match.end())

                continue

            # Find start of comment token, skip all after this until next newline
            match = comment.match(data)
            if match:
                skip = True
                order, data = breaks(data, match.end())

                continue

            # Find allel direcive, this stops consuming data
            match = allel.match(data)
            if match:

                return (orders, data)

            break

        return (orders, '')

    @staticmethod     
    def parse(data: str) -> list[list[str]]:
        allele: list[list[str]] = []

        while data:
            if data.startswith('#allel\n'):
                allel, data = Reader.consume_allel(data[7:])
                allele += [allel,]
                continue

            break

        return allele

    @staticmethod
    def open(path: str) -> list[str]:
        
        with open(path, 'r') as file:
            data = file.read()

        return Reader.parse(data)
   
def getGene(path: str, profile: Profile) -> Gene:
    '''Read gene from a file'''
    S1, S2 = Reader.open(path)
    return Gene.fromAmino(S1, S2, profile)