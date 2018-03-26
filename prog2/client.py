#!/usr/bin/python2
from __future__ import print_function
import threading
import socket
import struct
import sys

# Get our functions for the protocol
from server import send_msg, recv_msg, RECV

'''
USAGE:
    client.py [host] [nickname]

    host:       connect to specified host as server (default: localhost)
    nickname:   nickname/displayname for client (default: 'Alice')
'''

# Set the server host and client nickname
ADDR = ''
NICK = 'Alice'

# First argument is host
if len(sys.argv) > 1:
    ADDR = sys.argv[1]

# Second argument is nickname
if len(sys.argv) > 2:
    NICK = sys.argv[2]

# Messages to send
msg_queue = []

# Hanlder for the TCP connection to the server
def handle_client():
    # Get our connection and send nickname
    try:
        csock = socket.socket()
        csock.connect((ADDR, RECV))
        send_msg(csock, NICK)
    # We might have an incorrect host
    except socket.error as error:
        print('Socket error: {}'.format(error))
        print('Please check the host parameter, or restart mininet.')
        sys.exit(1)

    # Placeholders for received messages 
    recv_msgs = ''
    
    # Check the continue flag every loop
    cont = True

    # Send/Receive loop until continue is false ('Bye' message received by server)
    while cont:
        # If we have messages to send, pop and send them
        if len(msg_queue) > 0:
            msg = msg_queue.pop()
            if msg == 'Bye':
                send_msg(csock, msg, False)
            else:
                send_msg(csock, msg)
        # If we have nothing, send 'nothing' to let the server continue
        # through the other clients
        else:
            send_msg(csock)

        # Get new messages from the server, print them on the screen
        cont, recv_msgs = recv_msg(csock)
        if recv_msgs:
            print(recv_msgs)

    # Close the connection when the session ends
    csock.close()
    sys.exit()

# This function will be run as a thread to handle input
# from the keyboard
def handle_input():
    while True:
        nextmsg = raw_input('')
        msg_queue.append(nextmsg)

# Create our input handler thread and start it
cthread = threading.Thread(target = handle_input)
cthread.daemon = True # daemon thread will exit with the main thread
cthread.start()

# Start the chat handler
handle_client()
