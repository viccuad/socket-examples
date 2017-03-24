#! /usr/bin/env python3

"""
Usage: {name} <server> <word> <port>

This client simulates a low-bandwidth connection by introducing artificial delays
in sending data, and dribbiling out its messages byte by byte.

To achieve that, be thread multiple connections, each of them slow.
"""


from socket import socket, AF_INET, SOCK_STREAM
from sys import argv
import time
import concurrent.futures

BUFFSIZE = 255

start = time.time()

def request(n, message, server):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((argv[1], int(argv[3])))
    messagelen, received = len(message), 0
    for c in message:
        sock.send(c)
        time.sleep(.1)
    data = ""
    while received < messagelen:
        data += sock.recv(1)
        time.sleep(.1)
        received += 1
    sock.close()
    print("Received: {0} from {1}".format(data.decode("utf-8"), server))

if len(argv) != 4:
    print(__doc__.format(name=argv[0]))
    exit(1)

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = []
    for n in range(20):
        future = executor.submit(request, n, argv[2], argv[1])
        futures.append(future)
        # print(future.result())
    concurrent.futures.as_completed(futures)
    concurrent.futures.wait(futures,return_when=concurrent.futures.ALL_COMPLETED)

print("{} seconds".format(time.time() - start))
