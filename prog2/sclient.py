#!/usr/bin/python
from __future__ import print_function
import socket
import sys

# Message protocol
from server import recv_msg, send_msg

if len(sys.argv) < 4:
    print('''USAGE:
        ./sclient.py [host] [client] [name]

        host: server host to connect to
        client: client name
        name: your name''')
    sys.exit(1)

# Parameters for the connection/message
HOST = sys.argv[1]
CLIENT = sys.argv[2]
NAME = sys.argv[3]

# Connect to server
csock = socket.socket()
csock.connect((HOST, 11000))

# Send message
to_server = 'Client {}: {}'.format(CLIENT, NAME)
send_msg(csock, to_server)

# Receive Ack
_,ack = recv_msg(csock)

# Print message and ack
print(to_server)
print(ack)

# Close connection
csock.close()
