from sys import exit
from typing import Any, NoReturn

from pygame import display, event, init, mouse, quit
from pygame.locals import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    QUIT,
    RESIZABLE,
    VIDEORESIZE,
)

from .jigsaw import JigSaw
from .tiles import JigSawTiles, Tile

# for tile snapping
TOP = BOTTOM = 1
LEFT = RIGHT = 0

SCREEN_DIMENSIONS = (800, 600)


class GameClient:
    """When the puzzle is chosen the game starts here"""

    def __init__(self, action: dict[str, Any]) -> None:
        """Initialization method

        This gets the resized and cropped image then tiles it
        """
        init()

        self.screen = display.set_mode(SCREEN_DIMENSIONS, RESIZABLE)
        self.jigsaw = JigSaw(self.screen, action["image"].size)
        self.tiles = JigSawTiles()
        self.solved_tiles = action["solved_tiles"]

        for pos, tile in action["scrambled_tiles"]:
            self.tiles.add(Tile(pos, action["overlap"], tile))

    def mainloop(self) -> NoReturn:
        """The main game loop that currently looks for mouse and quit events"""
        while True:
            for e in event.get():
                if e.type == QUIT:
                    quit()
                    exit()
                mouse_position = mouse.get_pos()
                if e.type == MOUSEBUTTONDOWN:
                    if self.jigsaw.rect.collidepoint(mouse_position):
                        self.jigsaw.mouse_down(self.tiles, mouse_position)
                if e.type == MOUSEBUTTONUP:
                    self.jigsaw.mouse_up(self.tiles)
                if e.type == MOUSEMOTION:
                    self.jigsaw.mouse_motion(self.tiles, mouse_position)
                if e.type == VIDEORESIZE:
                    self.jigsaw.set_bounds()

            self.screen.fill("black")
            self.jigsaw.fill("white")
            self.tiles.draw(self.jigsaw)
            self.screen.blit(self.jigsaw, self.jigsaw.center)

            display.update()
