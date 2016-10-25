from time import sleep

import pygame
from pygame.locals import *
from driver import Driver

# Code modified from: http://pygametutorials.wikidot.com/tutorials-basic

class App:
    def __init__(self):
        # Pygame stuff
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400

        # Initialize driver
        self.driver = Driver()

    def on_init(self):
        pygame.init()

        # Starts window with dimensions, and attempts to use hardware
        # acceleration. 
        self._display_surf = pygame.display.set_mode(self.size, 
                             pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_key_press(self, key):
        if key == pygame.K_ESCAPE:
            print 'Quitting'
            self._running = False
        elif key == pygame.K_UP:
            print 'Key pressed up'
            self.driver.up()
        elif key == pygame.K_RIGHT:
            print 'Key pressed right'
            self.driver.right()
        elif key == pygame.K_DOWN:
            print 'Key pressed down'
            self.driver.back()
        elif key == pygame.K_LEFT:
            print 'Key pressed left'
            self.driver.left()

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.on_key_press(pygame.K_ESCAPE)
            if keys[pygame.K_UP]:
                self.on_key_press(pygame.K_UP)
            if keys[pygame.K_RIGHT]:
                self.on_key_press(pygame.K_RIGHT)
            if keys[pygame.K_DOWN]:
                self.on_key_press(pygame.K_DOWN)
            if keys[pygame.K_LEFT]:
                self.on_key_press(pygame.K_LEFT)
            self.on_loop()
            self.on_render()

            pygame.event.pump()
            sleep(0.05)
        self.on_cleanup()

if __name__ == '__main__':
    runApp = App()
    runApp.on_execute()

