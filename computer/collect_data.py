import socket
import time
import sys
import struct

import numpy as np
import pygame
from pygame.locals import *
from driver import Driver
from app import App

class CollectApp(App):
    def __init__(self, tcp_address, write_file):
        # Pygame stuff
        self._running = True
        self._display_surf = None

        # Initialize driver
        self.driver = Driver()

        # Directory to write data
        self.data_dir = './data/' + write_file + '.txt'

        # Create TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket to a port
        server_address = (tcp_address, 6666)
        print 'Staring up on %s port %s' % server_address
        self.sock.bind(server_address)

    def on_init(self):
        pygame.init()
         
        self._running = True

        # Listen for incoming TCP connections
        self.sock.listen(1)

    # Recvall(connection, x) receives anywhere from 1 to x bytes, so we need
    # to make sure we're getting exactly x bytes.
    def recv_exact(self, conn, length):
        buffer = b''
        while len(buffer) < length:
            data = conn.recv(length - len(buffer))
            if not data:
                return data
            buffer += data
        return buffer

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        print 'Waiting for connection'
        connection, client_address = self.sock.accept()
 
        try: 
            print 'Connection from ', client_address
            
            with open(self.data_dir, 'a') as fout:
                while(self._running):
                    start_time = time.time()
                    # 4 bit integer that represents which keys were pressed
                    keys_pressed = 0

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        self.on_key_press(pygame.K_ESCAPE)
                    if keys[pygame.K_UP]:
                        keys_pressed += 4
                    if keys[pygame.K_RIGHT]:
                        keys_pressed += 2
                    if keys[pygame.K_DOWN]:
                        keys_pressed += 8
                    if keys[pygame.K_LEFT]:
                        keys_pressed += 1
                    self.driver.write(keys_pressed)

                    # Clear event queue to process key pressed
                    pygame.event.pump()

                    # Input from the TCP connection: two integers (4 bytes)
                    # that represent width, height, in that order. Then, we have 
                    # width*height bytes that represent the pixel values at those
                    # positions. 
                    width = struct.unpack("!i", self.recv_exact(connection,4))[0]
                    height = struct.unpack("!i", self.recv_exact(connection,4))[0]
                    pixels = np.zeros((height, width))
                    pixels_disp = np.zeros((width, height, 3))

                    if not self._display_surf:
                        # Starts window with dimensions, and attempts to use hardware
                        # acceleration.
                        self._display_surf =  pygame.display.set_mode((width, height), 
                                              pygame.HWSURFACE | pygame.DOUBLEBUF)

                    for idx1 in range(0, height):
                        for idx2 in range(0, width):
                            data = self.recv_exact(connection,1)
                            pixels[idx1, idx2] = int(data.encode('hex'), 16)

                    pixels = np.flipud(pixels)
                    pixels_disp[:,:,0] = np.rot90(pixels)
                    pixels_disp[:,:,1] = pixels_disp[:,:,0]
                    pixels_disp[:,:,2] = pixels_disp[:,:,0]

                    pygame.surfarray.blit_array(self._display_surf,pixels_disp)
                    pygame.display.update()

                    #Save image along with keys_pressed, and width and height
                    if not keys_pressed == 0:
                        tosave = pixels.flatten()
                        tosave = np.append([keys_pressed, width, height], tosave)
                        np.savetxt(fout, tosave[None], fmt='%d', delimiter=' ')

                    loop_time = time.time() - start_time
                    print 'Loop time: %f', loop_time

        finally:
            # Clean up connection
            connection.close()
            
        self.on_cleanup()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Error: insufficient arguments'
        print 'Usage: python collect_data.py [arg1] [arg2]'
        print 'Where argument 1 is the IP address of the TCP server'
        print 'And argument 2 is the name of the file to write data'
    else:
        server_address = sys.argv[1]
        write_file = sys.argv[2]
        runApp = CollectApp(server_address, write_file)
        runApp.on_execute()
