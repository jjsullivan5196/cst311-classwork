#!/usr/bin/python2
from __future__ import print_function
from datetime import datetime
import socket
import struct

# Listen socket port
RECV = 12000

# Create a listen socket
def create_and_bind(addr):
    sock = socket.socket()
    sock.bind(addr)
    sock.settimeout(0.05)
    sock.listen(0)
    return sock

# Functions to enforce message protocol between client/server
def send_msg(sock, msg = ''):
    sock.sendall(struct.pack('!I{}s'.format(len(msg)), len(msg), msg))

def recv_msg(sock):
    size, = struct.unpack('!I', sock.recv(struct.calcsize('!I')))
    if size > 0:
        recv_fmt = '{}s'.format(size)
        return struct.unpack(recv_fmt, sock.recv(struct.calcsize(recv_fmt)))[0]
    else:
        return ''

# Main handler for the server
def handle_connections():
    # Create listen socket and client list
    recv_sock = create_and_bind(('', RECV))
    clients = []
    msgs = ''

    # Serve requests
    while True:
        # Connect incoming clients, record their connection, client number, and nickname
        try:
            next_client = recv_sock.accept()
            next_conn,_  = next_client
            nickname, number = recv_msg(next_conn), len(clients)
            new_client = (next_client[0], next_client[1], {'Client' : number, 'Name' : nickname })
            clients.append(new_client)
            print('New client')
        except socket.timeout: # Skip ahead incase of timeout
            pass

        # Store messages from each client
        next_round = []

        # We'll put a timestamp for when each message is recieved
        time_now = datetime.now()
        for client in clients:
        # Go around all client connections, get new messages and
        # pass them on to the other clients.
            # Get connection
            conn = client[0]

            # Read message
            cmsg = recv_msg(conn)
            if cmsg != '':
                # Format the message for broadcast
                cmsg = '{} {}: {}'.format(time_now, client[2], cmsg)
                next_round.append(cmsg)

            # Send last round to clients
            send_msg(conn, msgs)

        # Kill the session if someone says 'Bye'
        if 'Bye' in msgs:
            break

        # Flush the last round of messages, join the next round
        # into one large message
        msgs = ''
        if len(next_round) > 0:
            msgs = '\n'.join(next_round)

    # Stop taking connections
    recv_sock.close()

    # Ensure all clients are disconnected
    for client in clients:
        conn = client[0]
        conn.close()

# Run the server
if __name__ == '__main__':
    handle_connections()
