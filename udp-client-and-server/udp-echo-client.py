#! /usr/bin/env python3

"""
Usage: {name} <server> <word> <port>
"""

# from socket import socket, AF_INET, SOCK_DGRAM
from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv #, exit
MAXBUFSIZE = 255

if len(argv) != 4:
    print(__doc__.format(name=argv[0]))
    exit(0)

sock = socket(AF_INET, SOCK_DGRAM)
messout = argv[2]

# Since it is UDP, it is connectionless, just sendto and recvfrom
sock.sendto(messout.encode('utf-8'), (argv[1], int(argv[3])))
t = sock.recvfrom(MAXBUFSIZE)
messin, server = t[0].decode('utf-8'), t[1]

if messin != messout:
    print("Failed to receive identical message")
print("Received: {0} from {1}".format(messin, server))
sock.close()
