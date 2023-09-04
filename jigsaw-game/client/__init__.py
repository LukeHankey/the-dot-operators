#!/usr/bin/venv python3
"""This is all the GUI magic"""

from sys import exit

from common import get_image, regular, square_tiles
from pygame import Rect, Surface, display, event, image, init, mouse, quit, sprite
from pygame.locals import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    QUIT,
    RESIZABLE,
    VIDEORESIZE,
)

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255, 255, 255)
BLACK = (000, 000, 000)


class Tile(sprite.Sprite):
    """Tile which is a cropped image at a specifc point.

    dragging support is built in TODO; add support for alpha, better
    bounding box methods
    """

    def __init__(self, pos: tuple[int, int], cropped_image):
        """Basic init method that takes pillow image into pygame image"""
        super().__init__()
        self.image = image.fromstring(
            cropped_image.tobytes(), cropped_image.size, cropped_image.mode
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.active = False
        self.drag_offset: tuple[int, int]

    def activate(self, pointer: tuple[int, int]):
        """Could add tile highlighting and other affects"""
        self.active = True
        self.drag_offset = (
            pointer[0] - self.rect.topleft[0],
            pointer[1] - self.rect.topleft[1],
        )

    def deactivate(self):
        """Remove anything `activate` added"""
        self.active = False
        self.drag_offset = (0, 0)  # so move can be used more directly

    def move(self, pointer: tuple[int, int]):
        """Move tile to pointer could be a mouse pointer or anything"""
        self.rect.topleft = (
            pointer[0] - self.drag_offset[0],
            pointer[1] - self.drag_offset[1],
        )


class MenuClient:
    """Dummy Object for now could be placed into seperate module"""


class JigSaw(Surface):
    """This is the Surface that the user interacts with the puzzle"""

    def __init__(self, screen: Surface, size: tuple[int, int]):
        """Set Jigsaw position"""
        super(JigSaw, self).__init__(size)
        self.screen = screen
        self.size = size
        self.set_bounds()

    def set_bounds(self):
        """Called to set the real surface coords"""
        screen_bounds = self.screen.get_rect()
        surface_bounds = self.get_rect()
        x_offset = (screen_bounds.width - surface_bounds.width) // 2
        y_offset = (screen_bounds.height - surface_bounds.height) // 2
        self.rect = Rect(
            x_offset, y_offset, self.size[0] + x_offset, self.size[1] + y_offset
        )
        self.center = (x_offset, y_offset)

    def translate(self, position: tuple[int, int]):
        """Adjust screen coordinates to jigsaw surface coordinates"""
        offset = (
            position[0] - self.rect.topleft[0],
            position[1] - self.rect.topleft[1],
        )
        return offset


class GameClient:
    """When the puzzle is chosen the game starts here"""

    def __init__(self, filename: str, num_of_tiles: int):
        """Initialization method

        This gets the resized and cropped image then tiles it
        """
        init()
        self.screen = display.set_mode(SCREEN_DIMENSIONS, RESIZABLE)
        self.tiles = sprite.Group()
        image = get_image(filename, SCREEN_DIMENSIONS, num_of_tiles)
        self.jigsaw = JigSaw(self.screen, image.size)
        for pos, image_tile in regular(square_tiles, image, num_of_tiles):
            self.tiles.add(Tile(pos, image_tile))

    def mainloop(self):
        """The main game loop that currently looks for mouse and quit events"""
        while True:
            for e in event.get():
                if e.type == QUIT:
                    quit()  # exit cleanly
                    exit()
                if e.type == MOUSEBUTTONDOWN:
                    if self.jigsaw.rect.collidepoint(mouse.get_pos()):
                        # [::-1] reverse list check is downwards in z depth
                        for tile in self.tiles.sprites()[::-1]:
                            if tile.rect.collidepoint(
                                self.jigsaw.translate(mouse.get_pos())
                            ):
                                # reorder to the top before drag
                                self.tiles.remove(tile)
                                self.tiles.add(tile)  # reorder to top
                                tile.activate(mouse.get_pos())
                                break
                if e.type == MOUSEBUTTONUP:
                    for tile in self.tiles.sprites()[::-1]:
                        tile.active = False
                if e.type == MOUSEMOTION:
                    for tile in self.tiles.sprites()[::-1]:
                        if tile.active:
                            tile.move(mouse.get_pos())
                if e.type == VIDEORESIZE:
                    self.jigsaw.set_bounds()

            self.screen.fill(BLACK)
            self.jigsaw.fill(WHITE)
            self.tiles.draw(self.jigsaw)
            self.screen.blit(self.jigsaw, self.jigsaw.center)
            display.update()
