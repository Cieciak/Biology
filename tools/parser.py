from typing import Callable
import re

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
                print('Newline found, skipping')
                order, data = breaks(data, match.end())

                continue

            # Find start of comment token, skip all after this until next newline
            match = comment.match(data)
            if match:
                skip = True
                print('Comment found, skipping all')
                order, data = breaks(data, match.end())

                continue

            # Find allel direcive, this stops consuming data
            match = allel.match(data)
            if match:
                print('Beggining of next allel found!')

                return (orders, data)

            break

        return (orders, '')

    @staticmethod     
    def process(data: str):

        while data:
            if data.startswith('#allel\n'):
                allel, data = Reader.consume_allel(data[7:])
                print(allel)

                continue

            break

    @staticmethod
    def open(path: str) -> list[str]:
        
        with open(path, 'r') as file:
            data = file.read()

        return Reader.parse(data)

    @staticmethod
    def parse(data: str) -> list[str]:
        '''Return list of amino-acids from string'''

        Reader.process(data[::])

        # Split into lines
        lines: list[str] = data.split('\n')

        orders: list[str] = []
        for line in lines:
            if not line: continue # Skip empty

            # Everthing after ';' is a comment
            left, *rigth = line.split(';', 1)

            # Split line on ' ', and add to orders if not empty
            orders += [bit.strip() for bit in left.split(' ') if bit]
            
        return orders
    
getGene: Callable = Reader.open