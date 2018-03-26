#!/usr/bin/python2
from __future__ import print_function
import socket
import sys

# Message protocol
from server import recv_msg, send_msg

# Store messages, clients
msgs = []
clients = []

# Setup listen socket
lsock = socket.socket()
lsock.bind(('', 11000))
lsock.listen(0)

# Take two connections, receive messages
for i in range(2):
    conn,_ = lsock.accept()
    clients.append(conn)
    msgs.append(recv_msg(conn)[1])
    print(msgs[i])

# Stop taking connections
lsock.close()

# Send back the Ack
client_name = [name[7:] for name in msgs]
msg = '{} received before {}'.format(*client_name)
print(msg)

for client in clients:
    send_msg(client, msg)
    client.close() # DC client

# Print exit message
print('Sent acknowledgement to {} and {}'.format(*[name[7] for name in msgs]))
