import os, threading
from ..CPPP import CPPP

KEY_PATH = os.path.dirname(__file__) + '/scp3.keyset'
SOCKET = CPPP.SCP3.from_keyfile(KEY_PATH)

SOCKET.connect('127.0.0.1', 8000)

SOCKET.send_string('give')

print(SOCKET.raw_recv())