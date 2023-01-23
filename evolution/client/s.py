import os, threading, json
from ..CPPP import CPPP

KEY_PATH = os.path.dirname(__file__) + '/scp3.keyset'
SOCKET = CPPP.SCP3.from_keyfile(key_file = KEY_PATH)

SOCKET.connect('127.0.0.1', 8000)
SOCKET.send(bytearray('give', 'utf-8'))

print(SOCKET.raw_recv())