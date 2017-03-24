#! /usr/bin/env python3

"""
Usage: echoclient.py echoserver.py <port>

Python socket server implemented with Socket
"""

from socket import socket, AF_INET, SOCK_STREAM
import sys
BUFFSIZE = 32
MAXCONNECTIONS = 5


def handleClient(sock):
    """handle client sockets"""

    data = sock.recv(BUFFSIZE)
    while data:
        sock.sendall(data)
        data = sock.recv(BUFFSIZE)
    sock.close()


if len(sys.argv) != 2:
    print(__doc__)
else:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind('', int(sys.argv[1]))
    sock.listen(MAXCONNECTIONS)
    while 1:
        newsock, client_addr = sock.accept()
        print("Client connected: ", client_addr)
        handleClient(newsock)
