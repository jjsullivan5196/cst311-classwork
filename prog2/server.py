#!/usr/bin/python2
from __future__ import print_function
from datetime import datetime
import socket
import struct
import sys

# These classes handle queuing up and formatting messages from clients
from msgqueue import MsgQueue, DebugQueue

# Listen socket port
RECV = 12000

# Create a listen socket
def create_and_bind(addr):
    try:
        sock = socket.socket()
        sock.bind(addr)
        sock.settimeout(0.05)
        sock.listen(0)
        return sock
    # Probably another server running
    except socket.error as error:
        print('Socket error: {}'.format(error))
        print('Please make sure no other servers are running.')
        sys.exit(1)

# Functions to enforce message protocol between client/server
#
# Our normal message is formatted as follows:
# struct format: '!?I{X}s'
#
# Bytes 0-0: Set this to false to end the conversation
# Bytes 1-4: Length of the follwing message (0 if no message)
# Bytes 5-X: The message sent or received
#
def send_msg(sock, msg = '', cont = True):
    # Send the message in the protocol format
    sock.sendall(struct.pack('!?I{}s'.format(len(msg)), cont, len(msg), msg))

def recv_msg(sock):
    # Receive the continue byte and size of message
    cont, size = struct.unpack('!?I', sock.recv(struct.calcsize('!?I')))
    
    # If present, receive the message
    if size > 0:
        recv_fmt = '{}s'.format(size)
        return cont, struct.unpack(recv_fmt, sock.recv(struct.calcsize(recv_fmt)))[0]
    else:
        return cont, ''

# Main handler for the server
def handle_connections(queue = MsgQueue()):
    # Create listen socket and client list
    recv_sock = create_and_bind(('', RECV))
    clients = []
    msgs = ''
    cont = True

    # Serve requests, keep serving until continue byte is false
    while cont:
        # Connect incoming clients, record their connection, client number, and nickname
        try:
            next_client = recv_sock.accept()
            next_conn,_ = next_client
            clients.append((next_client[0], next_client[1], {
                'Client'    : len(clients), 
                'Name'      : recv_msg(next_conn)[1] 
            }))
        # Skip ahead incase of timeout
        except socket.timeout:             
            pass
        # For when things go wrong
        except socket.error as error:
            print('Socket error: {}'.format(error))
            print('Unexpected failure has occured')
            sys.exit(1)

        # Go around all client connections, get new messages and
        # pass them on to the other clients.
        for client in clients:
            # Get connection
            conn = client[0]

            # Read message and continue byte, AND continue byte
            # to determine if session should end
            ct, cmsg = recv_msg(conn)
            cont = ct and cont
            if cmsg:
                # Store the message for broadcast
                queue.append((datetime.now(), client[2], cmsg))

            # Send last round to clients
            send_msg(conn, msgs)

        # Flush the last round of messages, join the next round
        # into one large message
        msgs = ''
        if len(queue) > 0:
            msgs = queue.read()
            print(msgs)

    # Stop taking connections
    recv_sock.close()

    # Ensure all clients are disconnected
    for client in clients:
        conn = client[0]
        send_msg(conn, msgs, False)
        conn.close()

# Run the server
if __name__ == '__main__':
    handle_connections()
