import socket

RECV = 12000

recv_socket = socket.socket()
recv_socket.setblocking(False)
recv_socket.bind(('', RECV))
recv_socket.listen()

lastmsg = ''
clients = []

def handle_client(csock):
    pass

while lastmsg != 'Bye':
    nextclient = None
    nextclient = recv_socket.accept()


