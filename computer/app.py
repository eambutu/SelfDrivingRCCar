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

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print 'Quitting'
                self._running = False
            elif event.key == pygame.K_UP:
                print 'Key pressed up'
                self.driver.up()
            elif event.key == pygame.K_RIGHT:
                print 'Key pressed right'
                self.driver.right()
            elif event.key == pygame.K_DOWN:
                print 'Key pressed down'
                self.driver.back()
            elif event.key == pygame.K_LEFT:
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
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == '__main__':
    runApp = App()
    runApp.on_execute()

