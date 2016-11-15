import socket
import sys

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 6666)
print 'Connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    while True:
        message = raw_input('Enter a message: ')
        if message == '':
            break

        # Send data
        print 'Sending %s' % message
        sock.sendall(message)

        # Look for response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print 'Received %s' % data

finally: 
    print 'Closing socket'
    sock.close()
