#! /usr/bin/env python3

"""
Usage: {name} <port>
"""

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
MAXBUFSIZE = 256


def handleClient(sock):
    data = sock.recv(32)
    while data:
        sock.sendall(data)
        data = sock.recv(32)
    sock.close()


if __name__ == '__main__':
    if len(argv) != 2:
        print(__doc__.format(name=argv[0]))
        exit(1)

    sock = socket(AF_INET, SOCK_STREAM)
    # bind to a server socket. The server socket is not the actual socket the
    # message is transmitted over, rather, it acts as a factory for an ad-hoc
    # socket that is configured in recvfrom()
    sock.bind(('', int(argv[1])))
    sock.listen(2)
    while 1:
        newsock, client_addr = sock.accept()
        print("Client connected: {}".format(client_addr))
        handleClient(newsock)
