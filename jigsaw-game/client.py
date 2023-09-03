#!/usr/bin/venv python3
"""This is all the GUI magic"""

from sys import exit

from pygame import display, event, image, mouse, quit, sprite
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Tile(sprite.Sprite):
    """Tile which is a cropped image at a specifc point.

    dragging support is built in TODO; add support for alpha, better
    bounding box methods
    """

    def __init__(self, pos, cropped_image):
        """Basic init method that takes pillow image into pygame image"""
        super().__init__()
        self.image = image.fromstring(
            cropped_image.tobytes(), cropped_image.size, cropped_image.mode)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.dragging = False
        self.drag_offset = None


def mainloop(screen, tiles):
    """The main game loop that currently looks for mouse and quit events"""
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()  # exit cleanly
                exit()
            if e.type == MOUSEBUTTONDOWN:
                # [::-1] reverse list check is downwards in z depth
                for tile in tiles.sprites()[::-1]:
                    if tile.rect.collidepoint(mouse.get_pos()):

                        # reorder to the top before drag
                        tiles.remove(tile)
                        tiles.add(tile)  # reorder to top
                        tile.dragging = True

                        tile.drag_offset = (
                            mouse.get_pos()[0] - tile.rect.topleft[0],
                            mouse.get_pos()[1] - tile.rect.topleft[1])
                        break
            if e.type == MOUSEBUTTONUP:
                for tile in tiles.sprites()[::-1]:
                    tile.dragging = False
            if e.type == MOUSEMOTION:
                for tile in tiles.sprites()[::-1]:
                    if tile.dragging:
                        tile.rect.topleft = (
                            mouse.get_pos()[0] - tile.drag_offset[0],
                            mouse.get_pos()[1] - tile.drag_offset[1])

        screen.fill((255, 255, 255))
        tiles.draw(screen)
        display.update()
