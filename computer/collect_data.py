import socket
from driver import Driver

if __name__ == '__main__':
    # Create TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to port
    server_address = ('localhost', 6666)
    print 'Starting up on %s port %s' % server_address
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
