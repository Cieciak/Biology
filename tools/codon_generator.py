import yaml, random, csv, os

def flatten(iterable: list) -> list:
    output = []
    for object in iterable:
        if type(object) == list: output += flatten(object)
        else: output += [object, ]
    return output

def readConfig(path: str, profile: str = None):
    '''Read and parse `profiles.yaml`'''
    with open(path, 'r') as file:
        config = yaml.safe_load(file)

    if profile is None: profile = config['current']

    output = {}
    data = config[profile]

    output['length']    = data['length']
    output['table']     = data['table']
    output['overwrite'] = data['overwrite']

    output['bases']  = flatten(data['bases'])
    output['amino_acids'] = [code for code, name in data['amino-acids']]

    output['path'] = data['table']

    return output

def convertBase(n: int, base: int) -> list[int]:
    if n == 0: return [0, ]

    digits: list[int] = []
    while n:
        n, digit = divmod(n, base)
        digits += [digit, ]
    
    return digits

def createCodon(n: list[int], bases: list[str], lenght: int):
    '''Create nth codon'''
    codon = ''
    n += [0] * lenght
    for digit in n[:lenght]:
        codon += bases[digit]

    return codon

def createCodons(bases: list[str], length: int, **kwargs):
    '''Generate all possible codons'''
    codons = []
    for index in range(len(bases) ** length):
        current = convertBase(index, len(bases))
        codon = createCodon(current, bases, length)
        codons += [codon, ]

    return codons

def assignAminoAcids(codons: list[str], amino_acids: list[str], **kwargs):
    '''Randomly assign aminoacids to codons'''

    unpaired = amino_acids[::]
    pairs = []
    for codon in codons:
        amino = random.choice(unpaired)
        unpaired.remove(amino)
        if not unpaired: unpaired = amino_acids[::]
        pairs += [(codon, amino), ]

    return pairs

def dumpCSV(path: str, pairs: list[tuple], overwrite: bool = False, **kwargs):
    if (not overwrite) and os.path.exists(path): return

    with open(path, 'w') as file:
        CSV = csv.writer(file)
        for pair in pairs: CSV.writerow(pair)

def generateFromProfile(name: str = None, *, path = './profiles.yaml', overwrite: bool = False):
    profile_data = readConfig(path, name)
    codons = createCodons(**profile_data)
    pairs  = assignAminoAcids(codons, **profile_data)
    dumpCSV(pairs = pairs, **profile_data)

if __name__ == '__main__':
    generateFromProfile()
