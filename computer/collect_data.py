import socket
from time import sleep
import sys
import struct

import numpy as np
import pygame
from pygame.locals import *
from driver import Driver
from app import App

class CollectApp(App):
    def __init__(self, tcp_address):
        # Pygame stuff
        self._running = True
        self._display_surf = None

        # Initialize driver
        self.driver = Driver()

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
            
            while(self._running):
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
                self.on_loop()
                self.on_render()

                # Clear event queue to process key pressed
                pygame.event.pump()

                # Input from the TCP connection: two integers (4 bytes)
                # that represent width, height, in that order. Then, we have 
                # width*height bytes that represent the pixel values at those
                # positions. 
                width = struct.unpack("!i", self.recv_exact(connection,4))[0]
                height = struct.unpack("!i", self.recv_exact(connection,4))[0]
                pixels = np.zeros((height, width, 3))

                if not self._display_surf:
                    # Starts window with dimensions, and attempts to use hardware
                    # acceleration.
                    self._display_surf =  pygame.display.set_mode((height, width), 
                                          pygame.HWSURFACE | pygame.DOUBLEBUF)

                for idx1 in range(0, height):
                    for idx2 in range(0, width):
                        data = self.recv_exact(connection,1)
                        pixels[idx1, idx2, 0] = int(data.encode('hex'), 16)

                pixels[:,:,0] = np.flipud(pixels[:,:,0])
                pixels[:,:,1] = pixels[:,:,0]
                pixels[:,:,2] = pixels[:,:,0]

                pygame.surfarray.blit_array(self._display_surf,pixels)
                pygame.display.update()

                # TODO: save image along with keys_pressed

        finally:
            # Clean up connection
            connection.close()
            
        self.on_cleanup()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Error: insufficient arguments'
        print 'Usage: python collect_data.py [arg1]'
        print 'Where argument 1 is the IP address of the TCP server'
    else:
        server_address = sys.argv[1]
        runApp = CollectApp(server_address)
        runApp.on_execute()
