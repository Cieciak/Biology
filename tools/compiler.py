import yaml, random, csv, os

def importCodons(path: str = './profiles.yaml', profile: str = None):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)

    if profile is None: profile = config['current']
    data = config[profile]

    with open(data['table'], 'r') as file:
        CSV = csv.reader(file)
        codons = {codon: amino for codon, amino in CSV}

    return codons

def invertDictionary(dictionary: dict):
    inverted = {}
    for key, value in dictionary.items():
        if value in inverted:
            inverted[value] = inverted[value] + [key, ]
        else: inverted[value] = [key, ]
    
    return inverted

def compileRawFile(file: str, codons: dict, output: str = None,):
    name, ext = os.path.splitext(file)
    inverted = invertDictionary(codons)

    if output is None: output = f'{name}.gen'

    with open(file, 'r') as raw:
        lines = raw.readlines()

    genome = ''
    for amino in lines:
        amino = amino.strip().upper()
        genome += random.choice(inverted[amino])

    print(genome)

if __name__ == '__main__':
    codons = importCodons()
    print(codons)
    amino = invertDictionary(codons)
    print(amino)

    raw = compileRawFile('./assembly/raw/none.raw', codons)