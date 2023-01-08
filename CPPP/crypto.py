
class Automaton:

    def __init__(self, state):
        self.shift = state
        self.state = state

    def revert(self):
        self.shift = self.state

    def encode(self, array: bytearray) -> bytearray:
        output = bytearray()
        for byte in array:
            coded = (byte + self.shift) % 256
            output.append(coded)
            self.shift += 1
        return output

    def decode(self, array: bytearray) -> bytearray:
        output = bytearray()
        for byte in array:
            coded = (byte - self.shift) % 256
            output.append(coded)
            self.shift += 1
        return output

if __name__ == '__main__':
    c = Automaton(4)

    msg = bytearray('Hello', 'utf-8')

    encoded = c.encode(msg)
    c.revert()
    d = Automaton(4)
    decoded = d.decode(encoded)

    print(encoded)
    print(decoded)