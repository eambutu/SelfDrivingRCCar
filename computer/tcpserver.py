import socket
import sys

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to a port
server_address = ('localhost', 6666)
print 'Starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for connection
    print 'Waiting for connection'
    connection, client_address = sock.accept()

    try:
        print 'Connection from ', client_address

        # Receieve the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print 'Received %s' % data
            if data:
                print 'Sending data back to client'
                connection.sendall(data)
            else:
                print 'No more data from', client_address
                break
    
    finally:
        # Clean up connection
        connection.close()
