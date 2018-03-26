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
clientSocket.settimeout(1.0)

def stdev(values):
    length = float(len(values))
    mean = sum(values)/length
    dev = [(x - mean)**2 for x in values]

    return sum(dev)/length

def make_msg(seq, start):
    # Format message
    msg = 'hello'
    # Pad out to 1024 bytes
    msg += '\0' * (1024 - len(msg)) 
    return msg.encode()

def ping(seq, sock, address):
    # Begin ping
    start = time()
    sock.sendto(make_msg(seq, start), serverAddress)
    msg, addr = sock.recvfrom(1024)
    return msg.decode(), (time() - start) * 1000.0

FAIL = 0
RECV = 0
RTT = []

for x in range(1, PINGS + 1):
    while True:
        try:
            msg, rtt = ping(x, clientSocket, serverAddress)
            print('Message Received: "{}" Time: {}ms'.format(msg, rtt))
            RTT.append(rtt)
            RECV += 1
            break
        except socket.timeout:
            print('Request timed out')
            FAIL += 1

stats = {
    'host'      : serverAddress[0],
    'p_trans'   : RECV + FAIL,
    'p_recv'    : RECV,
    'pct_fail'  : int((float(FAIL)/float(RECV + FAIL)) * 100.0),
    'sum_time'  : sum(RTT),
    'min'       : min(RTT),
    'avg'       : sum(RTT)/len(RTT),
    'max'       : max(RTT),
    'mdev'      : stdev(RTT)
}

print('''--- {host} ping statistics ---
{p_trans} packets transmitted, {p_recv} received, {pct_fail}% packet loss, time {sum_time}ms
rtt min/avg/max/mdev {min}/{avg}/{max}/{mdev} ms'''.format(**stats))

clientSocket.close()
