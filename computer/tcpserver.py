import socket
import sys
import struct

# Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to a port
server_address = ('128.237.143.156', 6666)
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
        
        with open('./sample_input.txt', 'w') as fout:
            width = -1
            height = -1
            counter = 0
            toprint = ''

            # Receieve the data in small chunks and retransmit it
            while True:
                if not counter == 0 and counter > width * height:
                    break

                if width == -1 or height == -1:
                    data = connection.recv(4)
                    curint = struct.unpack("!i", data)[0]
                else:
                    data = connection.recv(1)
                    curint = int(data.encode('hex'), 16)

                if width == -1:
                    width = curint
                    fout.write(str(width))
                elif height == -1:
                    height = curint
                    fout.write(' ' + str(height))
                elif counter % width == 0:
                    fout.write(toprint + '\n')
                    toprint = str(curint)
                    counter += 1
                else:
                    toprint += ' ' + str(curint)
                    counter += 1

                if data:
                    print 'Sending data back to client'
                    connection.sendall(data)
                else:
                    print 'No more data from', client_address
                    break
    
    finally:
        # Clean up connection
        connection.close()
