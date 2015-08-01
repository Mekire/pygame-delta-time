#!/usr/bin/env python
"""
This example mirrors the 8-direction movement example here:
https://github.com/Mekire/meks-pygame-samples/blob/master/eight_dir_move.py

The difference is that this example uses delta time.
Delta time is a method of assuring that updates are unaffected by
changes in framerate.
"""


import os
import sys
import pygame as pg


CAPTION = "Delta Time"
SCREEN_SIZE = (500, 500)
TRANSPARENT = (0, 0, 0, 0)
BACKGROUND_COLOR = pg.Color("darkslategrey")


DIRECT_DICT = {pg.K_LEFT  : (-1, 0),
               pg.K_RIGHT : ( 1, 0),
               pg.K_UP    : ( 0,-1),
               pg.K_DOWN  : ( 0, 1)}


class Player(object):
    """This class will represent our user controlled character."""
    SIZE = (100, 100)
    
    def __init__(self, pos, speed):
        """
        Aside from setting up our image and rect as seen previously,
        in this example we create a new variable called true_pos.
        Rects can only hold integers, so in order to preserve fractional
        changes we need this new variable to hold the exact float position.
        Without it, a body that moved slower than 1 pixel per frame would
        never move.
        """
        self.image = self.make_image()
        self.rect = self.image.get_rect(center=pos)
        self.true_pos = list(self.rect.center) # Exact float position.
        self.speed = speed # Speed in pixels per second.
        
    def make_image(self):
        """
        Create player image. No differences from previous.
        """
        image = pg.Surface(Player.SIZE).convert_alpha()
        image.fill(TRANSPARENT)
        rect = image.get_rect()
        pg.draw.ellipse(image, pg.Color("black"), rect)
        pg.draw.ellipse(image, pg.Color("tomato"), rect.inflate(-12, -12))
        return image

    def update(self, keys, screen_rect, dt):
        """
        Update must accept a new argument dt (time delta between frames).
        Adjustments to position must be multiplied by this delta.
        Set the rect to true_pos once adjusted (automatically converts to int).
        """
        for key in DIRECT_DICT:
            if keys[key]:
                self.true_pos[0] += DIRECT_DICT[key][0]*self.speed*dt
                self.true_pos[1] += DIRECT_DICT[key][1]*self.speed*dt
        self.rect.center = self.true_pos
        self.clamp(screen_rect)

    def clamp(self, screen_rect):
        """
        Clamp the rect to the screen if needed and reset true_pos to the
        rect position so they don't lose sync.
        """
        if not screen_rect.contains(self.rect):
            self.rect.clamp_ip(screen_rect)
            self.true_pos = list(self.rect.center)

    def draw(self, surface):
        """
        Basic draw function.
        """
        surface.blit(self.image, self.rect)


class App(object):
    """
    Class responsible for program control flow.
    """
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        self.player = Player(self.screen_rect.center, 300) 

    def event_loop(self):
        """
        Basic event loop.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type in (pg.KEYDOWN, pg.KEYUP):
                self.keys = pg.key.get_pressed()

    def update(self, dt):
        """
        Update must acccept and pass dt to all elements that need to update.
        """
        self.player.update(self.keys, self.screen_rect, dt)
        
    def render(self):
        """
        Render all needed elements and update the display.
        """
        self.screen.fill(BACKGROUND_COLOR)
        self.player.draw(self.screen)
        pg.display.update()

    def main_loop(self):
        """
        We now use the return value of the call to self.clock.tick to
        get the time delta between frames.
        """
        dt = 0
        self.clock.tick(self.fps)
        while not self.done:
            self.event_loop()
            self.update(dt)
            self.render()
            dt = self.clock.tick(self.fps)/1000.0


def main():
    """
    Initialize; create an App; and start the main loop.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
