from sys import exit
from typing import NoReturn

from pygame import display, event, init, mouse, quit
from pygame.locals import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    QUIT,
    RESIZABLE,
    VIDEORESIZE,
)

from ..tessellation import square_tiler, tile_splitter
from ..utils import get_image
from .jigsaw import JigSaw
from .tiles import JigSawTiles, Tile

# for tile snapping
TOP = BOTTOM = 1
LEFT = RIGHT = 0

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255, 255, 255)
BLACK = (000, 000, 000)


class GameClient:
    """When the puzzle is chosen the game starts here"""

    def __init__(self, action: dict) -> None:
        """Initialization method

        This gets the resized and cropped image then tiles it
        """
        init()

        self.screen = display.set_mode(SCREEN_DIMENSIONS, RESIZABLE)
        self.tiles = JigSawTiles()

        num_of_tiles = action["num_of_tiles"]
        image = get_image(action["filename"], SCREEN_DIMENSIONS, num_of_tiles)
        self.jigsaw = JigSaw(self.screen, image.size)

        for pos, image_tile in tile_splitter(square_tiler, image, num_of_tiles):
            self.tiles.add(Tile(pos, action["overlap"], image_tile))

    def mainloop(self) -> NoReturn:
        """The main game loop that currently looks for mouse and quit events"""
        while True:
            for e in event.get():
                if e.type == QUIT:
                    quit()  # exit cleanly
                    exit()
                mouse_position = mouse.get_pos()
                if e.type == MOUSEBUTTONDOWN:
                    if self.jigsaw.rect.collidepoint(mouse_position):
                        self.tiles = self.jigsaw.mouse_down(self.tiles, mouse_position)
                if e.type == MOUSEBUTTONUP:
                    self.jigsaw.mouse_up(self.tiles, mouse_position)
                if e.type == MOUSEMOTION:
                    self.tiles = self.jigsaw.mouse_motion(self.tiles, mouse_position)
                if e.type == VIDEORESIZE:
                    self.jigsaw.set_bounds()

            self.screen.fill(BLACK)
            self.jigsaw.fill(WHITE)
            self.tiles.draw(self.jigsaw)
            self.screen.blit(self.jigsaw, self.jigsaw.center)

            display.update()
