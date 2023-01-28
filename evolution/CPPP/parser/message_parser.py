from enum import Enum, auto
import re, json

TEST1 = r'''head{method:GET,location:/}body[Hello,World]'''
TEST2 = r'''head:test'''

NAME_PATTERN  = r"^[a-zA-Z]+"
VALUE_PATTERN = r"^[a-zA-Z/]+"
SPACER_PATTERN= r"^[\n,]"
COLON_PATTERN = r"^:"
SQ_O_PATTERN  = r"^\["
SQ_C_PATTERN  = r"^\]"
CU_O_PATTERN  = r"^\{"
CU_C_PATTERN  = r"^\}"

class CPPP_JSON_Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytearray):
            return obj.decode('UTF-8')
        elif isinstance(obj, bytes):
            return obj.decode('UTF-8')
        return json.JSONEncoder.default(self, obj)

class TokenType(Enum):
    NAME = re.compile(NAME_PATTERN)
    VALUE = re.compile(VALUE_PATTERN)

    ENTRY = None
    COLLECTION = None
    LIST = None

    SPACER = re.compile(SPACER_PATTERN)
    COLON = re.compile(COLON_PATTERN)

    SQ_O = re.compile(SQ_O_PATTERN)
    SQ_C = re.compile(SQ_C_PATTERN)
    CU_O = re.compile(CU_O_PATTERN)
    CU_C = re.compile(CU_C_PATTERN)

class Token:
    
    def __init__(self, _type: TokenType, data = None) -> None:
        self.type = _type
        self.data = data

    def __repr__(self) -> str:
        return f'{self.type.name}: \"{self.data}\"'

class Tokenizer:

    def __init__(self, text: str) -> None:
        self.text = text

        self.dict = {}

    def consume(self, stream: list[TokenType]):
        pass

    def consume_entry(self, stream: list[Token]):
        name  = stream.pop(0)
        colon = stream.pop(0)
        value = stream.pop(0)

        print(name, colon, value)

    def tokenize(self):
        self.token_stream: list[Token] = []
        copy = self.text[::1]
        while copy:
            for key, option in TokenType.__members__.items():
                if option.value:
                    # Match pattern with the string
                    m = re.match(option.value, copy)
                    if not m: continue

                    # When pattern found
                    start, stop = m.span()
                    data = copy[start:stop]
                    self.token_stream += [Token(option, data),]
                    copy = copy[stop:].strip(' ')

        self.type_stream: list[TokenType] = [token.type for token in self.token_stream]
        while self.token_stream:
            self.consume
            
class Parser:

    def __init__(self, text: str) -> None:
        self.text = text

class TempParser:

    def __init__(self) -> None:
        pass

    def parse(self, raw_data: bytearray):
        parsed = json.loads(raw_data[:-2])
        return parsed['head'], parsed['body']

if __name__ == '__main__':
    T = Tokenizer(TEST2)
    T.tokenize()
