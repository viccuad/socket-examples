#! /usr/bin/env python3

"""
Usage: {name} <port>

UDP socket echo server that waits 5 secs before responding to a client
"""

from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
import concurrent.futures

BUFFSIZE = 256

def lengthy_action(sock, message, client_addr):
    from time import sleep
    print("Client connected: {}".format(client_addr))
    sleep(5)
    sock.sendto(message.upper(), client_addr)

if len(argv) != 2:
    print(__doc__.format(name=argv[0]))
    exit(1)

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', int(argv[1])))

executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
while 1:
    message, client_addr = sock.recvfrom(BUFFSIZE)
    executor.submit(lengthy_action, sock, message, client_addr)
