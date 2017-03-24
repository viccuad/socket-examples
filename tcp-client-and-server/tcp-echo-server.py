#! /usr/bin/env python3

"""
Usage: echoserver.py <port>

Python socket server implemented with SocketServer
"""

from SocketServer import BaseRequestHandler, TCPServer
import sys#, socket

class EchoHandler(BaseRequestHandler):
    """
    Defines children of SocketServer.BaseRequestHandler that have a .handle()
    method
    """

    def handle(self):
        print("Client connected: ", self.client_address)
        self.request.sendall(self.request.recv(2**16))
        self.request.close()


if len(sys.argv) != 2:
    print(__doc__)
else:
    TCPServer(('', int(sys.argv[1])), EchoHandler).serve_forever()
