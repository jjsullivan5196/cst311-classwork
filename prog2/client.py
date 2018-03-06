#!/usr/bin/python2
from __future__ import print_function
import threading
import socket
import struct
import sys

# Get our functions for the protocol
from server import send_msg, recv_msg, RECV

# Set the server host and client nickname
ADDR = ''
NICK = 'Alice'

# First argument is host
if len(sys.argv) > 1:
    ADDR = sys.argv[1]

# Second argument is nickname
if len(sys.argv) > 2:
    NICK = sys.argv[2]

# Queued up messages for the client to send
msg_queue = []

# This function will run as a thread that communicates
# with the server over a TCP socket
def handle_client():
    # Get our connection and send nickname
    csock = socket.socket()
    csock.connect((ADDR, RECV))
    send_msg(csock, NICK)

    # Placeholders for messages/status
    msg = ''
    recv_msgs = ''

    # Send/Receive loop until someone says 'Bye'
    while 'Bye' not in recv_msgs:
        # If we have messages to send, pop and send them
        if len(msg_queue) > 0:
            msg = msg_queue.pop()
            send_msg(csock, msg)
        # If we have nothing, send 'nothing' to let the server continue
        # through the other clients
        else:
            send_msg(csock)

        # Get new messages from the server, print them on the screen
        recv_msgs = recv_msg(csock)
        if recv_msgs != '':
            print('\r' + recv_msgs)

    # Close the connection when the session ends
    csock.close()

# Create our client handler thread and start it
cthread = threading.Thread(target = handle_client)
cthread.daemon = True
cthread.start()

# The main thread will handle keyboard input until
# the client enters 'Bye'
nextmsg = ''
while nextmsg != 'Bye':
    nextmsg = raw_input('')
    msg_queue.append(nextmsg)

# Wait for the handler thread to finish
cthread.join()
