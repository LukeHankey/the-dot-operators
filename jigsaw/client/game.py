from sys import exit
from typing import NoReturn

from pygame import display, event, init, mouse, quit, sprite
from pygame.locals import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    QUIT,
    RESIZABLE,
    VIDEORESIZE,
)

from ..tiles import Tile, square_tiles
from ..utils import get_image, regular
from .puzzle import JigSaw

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255, 255, 255)
BLACK = (000, 000, 000)


class MenuClient:
    """Dummy Object for now could be placed into seperate module"""


class GameClient:
    """When the puzzle is chosen the game starts here"""

    def __init__(self, filename: str, num_of_tiles: int) -> None:
        """Initialization method

        This gets the resized and cropped image then tiles it
        """
        init()
        image = get_image(filename, SCREEN_DIMENSIONS, num_of_tiles)

        self.screen = display.set_mode(SCREEN_DIMENSIONS, RESIZABLE)
        self.tiles = sprite.Group()
        self.jigsaw = JigSaw(self.screen, image.size)

        for pos, image_tile in regular(square_tiles, image, num_of_tiles):
            self.tiles.add(Tile(pos, image_tile))

    def mainloop(self) -> NoReturn:
        """The main game loop that currently looks for mouse and quit events"""
        while True:
            for e in event.get():
                if e.type == QUIT:
                    quit()  # exit cleanly
                    exit()

                mouse_pos: tuple[int, int] = mouse.get_pos()
                if e.type == MOUSEBUTTONDOWN:
                    if self.jigsaw.rect.collidepoint(mouse_pos):
                        # [::-1] reverse list check is downwards in z depth
                        for tile in self.tiles.sprites()[::-1]:
                            if tile.rect.collidepoint(self.jigsaw.translate(mouse_pos)):
                                # reorder to the top before drag
                                self.tiles.remove(tile)
                                self.tiles.add(tile)  # reorder to top
                                tile.activate(mouse_pos)
                                break

                if e.type == MOUSEBUTTONUP:
                    for tile in self.tiles.sprites()[::-1]:
                        if tile.active:
                            v_snapped = False
                            h_snapped = False
                            # the max distance from the check_tile to snap (15% of the tile's width)
                            h_snapping_distance = tile.rect.width / 100 * 15
                            # the max distance from the check_tile to snap (15% of the tile's height)
                            v_snapping_distance = tile.rect.height / 100 * 15

                            left_snap = abs(self.jigsaw.size[0] - tile.rect.width)
                            right_snap = abs(self.jigsaw.size[0] - tile.rect.width)
                            if (
                                left_snap < right_snap
                                and left_snap <= h_snapping_distance
                                or tile.rect.midleft[0] < 0
                            ):
                                # snaps the tile's left side to the left game border
                                tile.snap_h(0, 0)
                                h_snapped = True
                            elif (
                                right_snap <= h_snapping_distance
                                or tile.rect.midright[0] > self.jigsaw.size[0]
                            ):
                                # snaps the tile's right side to the right game border
                                tile.snap_h(1, self.jigsaw.size[0])
                                h_snapped = True

                            top_snap = abs(self.jigsaw.size[1] - tile.rect.height)
                            bottom_snap = abs(self.jigsaw.size[1] - tile.rect.height)
                            if (
                                top_snap < bottom_snap
                                and top_snap <= v_snapping_distance
                                or tile.rect.midtop[1] < 0
                            ):
                                # snaps the tile's top side to the top game border
                                tile.snap_v(0, 0)
                                v_snapped = True
                            elif (
                                bottom_snap <= v_snapping_distance
                                or tile.rect.midbottom[1] > self.jigsaw.size[1]
                            ):
                                # snaps the tile's bottom side to the bottom game border
                                tile.snap_v(1, self.jigsaw.size[1])
                                v_snapped = True

                            for check_tile in self.tiles.sprites()[::-1]:
                                if v_snapped and h_snapped:
                                    # if the tile has been snapped on the 2 axis, no need to check the other tiles
                                    break
                                if check_tile != tile:
                                    if not h_snapped:
                                        left_snap = abs(
                                            check_tile.rect.midright[0]
                                            - tile.rect.midleft[0]
                                        )
                                        right_snap = abs(
                                            check_tile.rect.midleft[0]
                                            - tile.rect.midright[0]
                                        )
                                        if (
                                            left_snap < right_snap
                                            and left_snap <= h_snapping_distance
                                        ):
                                            # snaps the tile's left side to the right side of the check_tile
                                            tile.snap_h(0, check_tile.rect.midright[0])
                                            h_snapped = True
                                        elif right_snap <= h_snapping_distance:
                                            # snaps the tile's right side to the left side of the check_tile
                                            tile.snap_h(1, check_tile.rect.midleft[0])
                                            h_snapped = True

                                    if not v_snapped:
                                        top_snap = abs(
                                            check_tile.rect.midbottom[1]
                                            - tile.rect.midtop[1]
                                        )
                                        bottom_snap = abs(
                                            check_tile.rect.midtop[1]
                                            - tile.rect.midbottom[1]
                                        )
                                        if (
                                            top_snap < bottom_snap
                                            and top_snap <= v_snapping_distance
                                        ):
                                            # snaps the tile's top side to the bottom side of the check_tile
                                            tile.snap_v(0, check_tile.rect.midbottom[1])
                                            v_snapped = True
                                        elif bottom_snap <= v_snapping_distance:
                                            # snaps the tile's bottom side to the top side of the check_tile
                                            tile.snap_v(1, check_tile.rect.midtop[1])
                                            v_snapped = True
                        tile.deactivate()
                if e.type == MOUSEMOTION:
                    for tile in self.tiles.sprites()[::-1]:
                        if tile.active:
                            tile.move(mouse_pos)
                if e.type == VIDEORESIZE:
                    self.jigsaw.set_bounds()

            self.screen.fill(BLACK)
            self.jigsaw.fill(WHITE)
            self.tiles.draw(self.jigsaw)
            self.screen.blit(self.jigsaw, self.jigsaw.center)
            display.update()
