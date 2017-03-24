#! /usr/bin/env python3

"""
Usage: {name} <server> <word> <port>
"""


from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
import time
import concurrent.futures

BUFFSIZE = 255

start = time.time()
sock = socket(AF_INET, SOCK_DGRAM)

def request(n):
    sock.sendto("{} [{}]".format(argv[2], n).encode('utf-8'),
                (argv[1], int(argv[3])))
    messin, server = sock.recvfrom(BUFFSIZE)
    print("Received: {0} from {1}".format(messin.decode("utf-8"), server))

if len(argv) != 4:
    print(__doc__.format(name=argv[0]))
    exit(1)

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = []
    for n in range(20):
        future = executor.submit(request, n)
        futures.append(future)
        # print(future.result())
    concurrent.futures.as_completed(futures)
    concurrent.futures.wait(futures,return_when=concurrent.futures.ALL_COMPLETED)

sock.close()
print("{} seconds".format(time.time() - start))
