import socket, select
import time, pprint, types, json
from .parser.message_parser import TempParser, CPPP_JSON_Encoder

def recvall(sock: socket.socket, bufsize: int) -> bytearray:
    output = b''
    while True:
        raw_data = sock.recv(bufsize)
        output += raw_data
        if not raw_data or output.endswith(b'\00\00'): return output

class CPPPMessage:
    parser: TempParser = TempParser()

    def __init__(self, raw_data = None, *, header: dict = None, body = None) -> None:
        self.__raw = raw_data

        if raw_data:
            self.header, self.body = self.parser.parse(raw_data)
        else:
            self.header = header
            self.body = body

    def __repr__(self) -> str:
        return f'{pprint.pformat(self.header, indent = 4)}\n{self.body}'

    @property
    def raw(self):
        raw_dict = {'head': self.header, 'body': self.body}
        self.__raw = bytearray(json.dumps(raw_dict, cls = CPPP_JSON_Encoder), 'UTF-8') + b'\00\00'

        return self.__raw

    def add_header(self, header: dict):
        for key, value in header.items():
            self.header[key] = value

    def add_body(self, content):
        self.body = content

class CPPPServer:

    MAX_BUFFER = 4096

    def __init__(self, address: str, port: int):
        # Save server address and port
        self.address = address
        self.port = port

        # Server functions
        self.request_handler: types.FunctionType = lambda x: x
        self.startup_handler: types.FunctionType = lambda x: x 

        # Create socket and make a list to keep track of the connections
        self.connections: list[socket.socket] = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((address, port))
        self.server_socket.listen(10)

        # Add self to connections
        self.connections += [self.server_socket,]

    def __call__(self, function: types.FunctionType):
        match function.__name__:
            case 'handler':
                self.request_handler = function
            case 'setup':
                self.startup_handler = function
            case _:
                raise NameError(f'{function.__name__} is not a server function')

    def serve(self):
        while True:
            read, write, error = select.select(self.connections, [], [])

            for socket in read:
                if socket == self.server_socket:
                    incoming, address = self.server_socket.accept()
                    self.connections.append(incoming)
                else:
                    raw_data = recvall(socket, self.MAX_BUFFER)
                    if raw_data:
                        request  = CPPPMessage(raw_data)
                        response = self.request_handler(request)
                        socket.sendall(response.raw)
                    else:
                        socket.close()
                        self.connections.remove(socket)

def send_request(address: str, port: int, message: CPPPMessage):
    s = socket.socket()
    s.connect((address, port))
    s.sendall(message.raw)
    response = recvall(s, 4096)
    s.close()

    return CPPPMessage(response)