#!/usr/bin/python2
from __future__ import print_function
import sys
import socket
from time import time

'''
USAGE:
    ./ping.py                   # Ping localhost
    ./ping.py XXX.XXX.XXX.XXX   # Ping a remote host at XXX.XXX.XXX.XXX
'''

PINGS = 10
serverAddress = ('', 12000)

if len(sys.argv) > 1:
    serverAddress = (sys.argv[1], 12000)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.bind(('', 11000))
clientSocket.settimeout(0.5)

def make_msg(seq, start):
    # Format message
    msg = 'Ping hello {} {}'.format(seq, start)
    # Pad out to 1024 bytes
    #msg += '\0' * (1024 - len(msg)) 
    return msg.encode()

def ping(seq, sock, address):
    # Begin ping
    start = time()
    sock.sendto(make_msg(seq, start), serverAddress)
    msg, addr = sock.recvfrom(1024)
    return msg.decode(), time() - start

for x in range(1, PINGS + 1):
    while True:
        try:
            print('Message Received: "{}" Time: {}'.format(*ping(x, clientSocket, serverAddress)))
            break
        except socket.timeout:
            print('Request timed out')

clientSocket.close()
