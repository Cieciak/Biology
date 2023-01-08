import socket, crypto, pprint
import numpy as np

byte = lambda x: bytearray([x,])

# TODO: https://en.wikipedia.org/wiki/Negative_base
def to_bytes(n: int):
    raw = []
    while n:
        n, r = divmod(n, 256)
        raw.append(r)

    return bytearray(raw[::-1])

def print_bytes(_iter: bytearray):
    for byte in _iter:
        print(f'{byte:<3}', end=' ')

class CPPP:

    MAX_LEN = 1024

    @staticmethod
    def translate_message(message: bytearray):
        # Make a copy of the message
        to_process = message.copy()

        # Create output bytes
        output: bytearray = bytearray()
        while to_process:

            # Split to chunks with max size 255 bytes
            chunk      = to_process[:255]
            to_process = to_process[255:]

            # If max size chunk 
            if len(chunk) == 255 and to_process: output += byte(0xFF) + chunk + byte(0x00)
            else: output += byte(len(chunk)) + chunk

        return output

    @staticmethod
    def create_header(address: tuple[int], port: int, config: int):
        output: bytearray = bytearray()

        # Take care of 4 first bytes
        for number in address:
            output += byte(number)

        output += byte(port // 256) # Top half of the port
        output += byte(port  % 256) # Bottom half of the port
        output += byte(config)      # Config byte
        output += byte(0xBD)        # Reserved

        return output

    @staticmethod
    def create_packet(address: tuple[int], port: int, messages: list[bytearray], *, config: int = 0x00):

        raw_bytearray: bytearray = bytearray()
        output_packets: list[bytearray] = []

        for message in messages:
            raw_bytearray += CPPP.translate_message(message)

        while raw_bytearray:
            body          = raw_bytearray[:1016]
            raw_bytearray = raw_bytearray[1016:]

            if not raw_bytearray: config = config | 0x80
            else: config = config & 0x7F

            output_packets.append(CPPP.create_header(address, port, config) + body)

            if raw_bytearray: config = config | 0x01
            else: config = config & 0xFE

        return output_packets

    @staticmethod
    def read_body(packet: bytearray):
        # Make a copy of the recieved packet
        raw = packet.copy()

        messages = []
        message = bytearray()

        # Get the first step
        step = raw.pop(0)
        flag = 1

        while raw:
            # Get the fist frame of data
            data = raw[:step]
            raw  = raw[step:]

            # If you can get the next byte
            if raw: flag = raw.pop(0)

            message += data
            # If its 0x00 it's long frame, then get legnth of the next segment
            if flag == 0 and raw: 
                step = raw.pop(0)
            # If not add gathered message to the list
            else:
                messages.append(message)
                message = bytearray()
                step = flag

        # After nothing is left return
        return messages

    def __init__(self, sock: socket.socket = None) -> None:
        # If socket not given make new one
        if sock is None: self.socket = socket.socket()
        else: self.socket = socket.socket()

        self.recv_address: tuple[int]
        self.recv_port: int

        self.serve = -1

    def __repr__(self) -> str:
        return f'{self.recv_address}:{self.recv_port}'

    def connect(self, host: str, port: int) -> None:
        self.recv_address = tuple(int(val) for val in host.split('.'))
        self.recv_port    = port

        self.socket.connect((host, port))


    # Sending 
    def send(self, *messages: tuple[bytearray]):
        # List of messages to send in the request
        RAW_PACKETS = CPPP.create_packet(self.recv_address, self.recv_port, messages)
        for packet in RAW_PACKETS:
            self.socket.send(packet)

    def sendconn(self, address, port, conn, *messages):
        # List of messages to send in the request
        RAW_PACKETS = CPPP.create_packet(address, port, messages)
        for packet in RAW_PACKETS:
            conn.send(packet)

    def send_string(self, *messages: tuple[bytearray]):
        raw_messages = [bytearray(string, 'UTF-8') for string in messages]
        self.send(*raw_messages)

    def sendconn_string(self, address, port, conn, *messages):
        raw_messages = [bytearray(string, 'UTF-8') for string in messages]
        self.sendconn(address, port, conn, *raw_messages)

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def bind(self, host, port):
        self.socket.bind((host, port))

    def listen(self):
        self.socket.listen()

    def recv(self, *, filter = lambda x: x):
        while True:
            conn, addr = self.socket.accept()
            request = bytearray()

            while True:
                raw_data = conn.recv(1024)

                header   = raw_data[:8]
                request += raw_data[8:]

                if header[6] & 0b1000_0000:
                    return header, list(map(filter, CPPP.read_body(request))), conn, addr

    def raw_recv(self, *, filter = lambda x: x):
        request = bytearray()
        while True:
            raw_data = self.socket.recv(1024)

            header   = raw_data[:8]
            request += raw_data[8:]

            if header[6] & 0b1000_0000:
                return header, list(map(filter, CPPP.read_body(request)))

class SCP3(CPPP):

    # CHANGED
    @staticmethod
    def translate_message(message: bytearray, *, key: int, encode: bool = True):
        copy = message.copy()

        # Handle the encoding
        if encode:
            agent = crypto.Automaton(key)
            copy  = agent.encode(copy)

        # Split into chunks
        output = bytearray()
        while copy:
            chunk = copy[:255]
            copy  = copy[255:]

            # If maximum length split to chained message
            if len(chunk) == 255 and copy: output += byte(0xFF) + chunk + byte(0x00)
            else: output += byte(len(chunk)) + chunk
        return output

    # CHANGED
    @staticmethod
    def create_header(address: tuple[int], port: int, config: int):
        output: bytearray = bytearray()

        # Take care of 4 first bytes
        for number in address:
            output += byte(number)

        output += byte(port // 256) # Top half of the port
        output += byte(port  % 256) # Bottom half of the port
        output += byte(config)      # Config byte
        output += byte(0xBD)        # Reserved

        return output

    @classmethod
    def from_keyfile(cls, key_file: str):
        import json

        data = {}
        with open(key_file, 'r') as file:
            data = json.load(file)

        return cls(
            out_key = data['key'],
            out_atoms = {int(key):val for (key, val) in data['shared'].items()},
            inc_atoms = {int(key):val for (key, val) in data['outgoing'].items()},
            inc_threshold = data['threshold']
        )

    # CHANGED
    def __init__(self,
                 out_key: int = None,
                 out_atoms: dict[int, int] = None,
                 inc_atoms: dict[int, int] = None,
                 inc_threshold: int = None,):
        super().__init__()

        # Outgoing values
        self.out_key = out_key
        self.out_atoms = out_atoms

        # Incoming values
        self.inc_atoms = inc_atoms
        self.inc_threshold = inc_threshold

    # CHANGED
    def create_packet(self, messages: tuple[bytearray], config: int = 0x00):
        raw_bytearray: bytearray = bytearray()
        output_packets: list[bytearray] = []

        # Put atoms in front
        atom_count = len(self.out_atoms)
        raw_bytearray += SCP3.translate_message(to_bytes(atom_count), key = self.out_key, encode = False)
        for argument, value in self.out_atoms.items():
            raw_bytearray += SCP3.translate_message(to_bytes(argument), key = self.out_key, encode = False)
            raw_bytearray += SCP3.translate_message(to_bytes(   value), key = self.out_key, encode = False)

        for message in messages:
            raw_bytearray += SCP3.translate_message(message, key = self.out_key)

        # Split until 
        while raw_bytearray:
            body          = raw_bytearray[:1016]
            raw_bytearray = raw_bytearray[1016:]

            # Set the END flag
            if not raw_bytearray: config = config | 0x80
            else:                 config = config & 0x7F

            header = SCP3.create_header(address = self.recv_address, port = self.recv_port, config = config)
            output_packets.append(header + body)

            # Set the CONTINUATION flag
            if raw_bytearray: config = config | 0x01
            else:             config = config & 0xFE

        return output_packets

    def read_body(self, content: bytearray):
        copy = content.copy()

        messages: list[bytearray] = []
        message = bytearray()

        # Get the first step
        step = copy.pop(0)
        flag = 1

        while copy:
            data = copy[:step]
            copy = copy[step:]

            # If you can get the next byte
            if copy: flag = copy.pop(0)

            message += data

            if flag == 0 and copy:
                step = copy.pop(0)
            else:
                messages.append(message)
                message = bytearray()
                step = flag

        recv_atom_count = int.from_bytes(messages.pop(0))
        recv_atoms = {}
        for _ in range(recv_atom_count):
            key = int.from_bytes(messages.pop(0))
            val = int.from_bytes(messages.pop(0))
            recv_atoms[key] = val

        atoms = {**recv_atoms, **self.inc_atoms}

        matrix = []
        vector = []
        for key, value in atoms.items():
            row = [key ** power for power in range(self.inc_threshold)]
            matrix.append(row)
            vector.append(value)

        matrix = np.array(matrix, dtype = np.int64)
        vector = np.array(vector, dtype = np.int64)

        coeff = np.linalg.solve(matrix, vector)
        print(coeff)
        key = round(coeff[0])
        print(key)

        decoded = []
        for msg in messages:
            # TODO: Force NumPy to use ints
            agent = crypto.Automaton(key)
            decoded.append(agent.decode(msg))
        return decoded

    # Sending 
    def send(self, *messages: tuple[bytearray]):
        # List of messages to send in the request
        RAW_PACKETS = self.create_packet(messages = messages, config = 0x00)
        for packet in RAW_PACKETS:
            self.socket.send(packet)

    def sendconn(self, address, port, conn, *messages):
        # List of messages to send in the request
        # TODO: Fix this by changing *cfg arg in self.create_packet
        self.recv_address = address
        self.recv_port = port
        RAW_PACKETS = self.create_packet(messages = messages, config = 0x00)
        for packet in RAW_PACKETS:
            conn.send(packet)


    def recv(self, *, filter = lambda x: x):
        while True:
            conn, addr = self.socket.accept()
            request = bytearray()

            while True:
                raw_data = conn.recv(1024)

                header   = raw_data[:8]
                request += raw_data[8:]

                if header[6] & 0b1000_0000:
                    body = [filter(message) for message in self.read_body(request)]
                    return header, body, conn, addr

    def raw_recv(self, *, filter = lambda x: x):
        request = bytearray()
        while True:
            raw_data = self.socket.recv(1024)

            header   = raw_data[:8]
            request += raw_data[8:]

            if header[6] & 0b1000_0000:
                return header, list(map(filter, self.read_body(request)))

class CP3Server:

    def __init__(self, address: str, port: int, handler = lambda x: x) -> None:
        self.socket = CPPP()
        self.socket.bind(address, port)

        self.alive = True

        self.handle = handler

    def __call__(self, other):
        self.handle = other

    def listen(self):
        self.socket.listen()

    def serve(self):

        while self.alive:
            head, body, conn, addr = self.socket.recv()
            address = [int(i) for i in addr[0].split('.')]
            port = addr[1]

            response = self.handle(body)

            self.socket.sendconn(address, port, conn, *response)

    def close(self):
        self.socket.close()

class SCP3Server:

    @classmethod
    def from_keyfile(cls, key_file: str, address: str, port: int):
        import json
        data = {}
        with open(key_file, 'r') as file:
            data = json.load(file)

        return cls(
            out_key = data['key'],
            out_atoms = {int(key):val for (key, val) in data['shared'].items()},
            inc_atoms = {int(key):val for (key, val) in data['incoming'].items()},
            inc_threshold = data['threshold'],
            address = address,
            port = port,
        )

    def __init__(self,
                 out_key,
                 out_atoms,
                 inc_atoms,
                 inc_threshold,
                 address,
                 port,
                 handler = lambda x: x) -> None:

        self.socket = SCP3(out_key = out_key,
                            out_atoms = out_atoms,
                            inc_atoms = inc_atoms,
                            inc_threshold = inc_threshold)
        self.socket.bind(address, port)
        self.alive = True

        self.handler = handler

    def __call__(self, other):
        self.handler = other

    def listen(self):
        self.socket.listen()

    def serve(self):
        while self.alive:
            head, body, conn, addr = self.socket.recv()
            address = [int(i) for i in addr[0].split('.')]
            port = addr[1]

            response = self.handler(body)

            self.socket.sendconn(address, port, conn, *response)

    def close(self):
        self.socket.close()

if __name__ == '__main__':
    PATH = './scp3.keyset'

    server = SCP3Server.from_keyfile(PATH, '0.0.0.0', 1024)
    
    @server
    def handle(x: list[bytearray]):
        response = []
        for msg in x:
            print(msg)
            response.append(msg)

        return response

    server.listen()
    try:
        server.serve()
    except KeyboardInterrupt:
        server.close()
        print('Server closed')