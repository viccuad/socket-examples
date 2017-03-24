#!/usr/bin/env python3

"""
Usage: {name} <port>
"""

from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import time
from select import select

if __name__=='__main__':
    if len(argv) != 2:
        print(__doc__.format(name=argv[0]))
        exit(1)
    while 1:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(('',int(argv[1])))
        print("Ready...")
        data = {}
        sock.listen(20)
        for _ in range(20):
            newsock, client_addr = sock.accept()
            print("Client connected: {}".format(client_addr))
            data[newsock] = ""
        last_activity = time.time()
        while 1:
            read, write, err = select(data.keys(), data.keys(), [])
            if time.time() - last_activity > 5:
                for s in read: s.shutdown(2)
                break
            for s in read:
                data[s] = s.recv(32)
            for s in write:
                if data[s]:
                    last_activity = time.time()
                    s.send(data[s])
                    data[s] = ""
