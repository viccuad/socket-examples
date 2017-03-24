#! /usr/bin/env python3

"""
Usage: {name} <port>
"""

from socketserver import DatagramRequestHandler, UDPServer
from sys import argv

class EchoHandler(DatagramRequestHandler):
    def handle(self):
        print("Client connected: ", self.client_address)
        message = self.rfile.read() # read from the connecting client
        self.wfile.write(message)   # write from the connecting client

if len(argv) != 2:
    print(__doc__.format(name=argv[0]))
else:
    UDPServer(('', int(argv[1])), EchoHandler).serve_forever()
