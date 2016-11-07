import socket
from time import sleep
import sys

import pygame
from pygame.locals import *
from driver import Driver
from app import App

class CollectApp(App):
    def __init__(self, tcp_address):
        # Pygame stuff
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400

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

        # Starts window with dimensions, and attempts to use hardware
        # acceleration. 
        self._display_surf = pygame.display.set_mode(self.size, 
                             pygame.HWSURFACE | pygame.DOUBLEBUF)
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
                    self.on_key_press(pygame.K_UP)
                    key_pressed += 1
                if keys[pygame.K_RIGHT]:
                    self.on_key_press(pygame.K_RIGHT)
                    key_pressed += 2
                if keys[pygame.K_DOWN]:
                    self.on_key_press(pygame.K_DOWN)
                    key_pressed += 4
                if keys[pygame.K_LEFT]:
                    self.on_key_press(pygame.K_LEFT)
                    key_pressed += 8
                self.on_loop()
                self.on_render()

                # Clear event queue to process key pressed
                pygame.event.pump()

                # Get image
                length = self.recv_exact(connection, 1000) #TODO: replace this
                if not length:
                    print 'Invalid length from TCP client'
                data = self.recv_exact(connection, int(length))
                if not data:
                    print 'Invalid data from TCP client'

                # TODO: save image along with keys_pressed

                # Collect data every 0.05 seconds
                sleep(0.05)

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
