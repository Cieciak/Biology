# The simplest echo server

import CPPP

server = CPPP.CPPPServer('0.0.0.0', 8000)

try: server.serve()
except KeyboardInterrupt: print('Server stopped!')