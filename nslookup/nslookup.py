#! /usr/bin/env python3
"Usage nslookup.py <inet_address>"

import socket
import sys

print(socket.gethostbyname(sys.argv[1]))
