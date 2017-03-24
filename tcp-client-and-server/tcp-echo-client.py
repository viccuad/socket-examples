#! /usr/bin/env python3

"""
Usage: echoclient.py <server> <word> <port>

<server> can be a dotted-quad IP (192.168.2.103) or a symbolic name
         (google.com)
"""

from socket import socket, AF_INET, SOCK_STREAM
import sys

if len(sys.argv) != 4:
    print(__doc__)
    sys.exit(1)

BUFFSIZE = 32
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((sys.argv[1], sys.argv[3]))
message = sys.argv[2]
messlen, received = sock.send(message), 0

if messlen != len(message):
    print("Failed to send complete message")

print("Received: ,")

while received < messlen:
    data = sock.recv(BUFFSIZE)
    sys.stdout.write(data)
    received += len(data)
print()
sock.close()
