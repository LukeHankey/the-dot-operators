#!/usr/bin/venv python3
"""This is all the GUI magic"""

from sys import exit

from common import get_image
from common.tessellation import square_tiler, tile_splitter
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

    def snap(self, side: str, coord: int, axis: int):
        """Snaps the tile to other tiles/image borders on the horizontal axis"""
        if side == "topleft":
            tmp_coord = list(self.rect.topleft)
            tmp_coord[axis] = coord
            self.rect.topleft = tuple(tmp_coord)
        else:
            tmp_coord = list(self.rect.bottomright)
            tmp_coord[axis] = coord
            self.rect.bottomright = tuple(tmp_coord)


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
        for pos, image_tile in tile_splitter(square_tiler, image, num_of_tiles):
            self.tiles.add(Tile(pos, image_tile))
        self.sides_axes = {
            "top": 1,
            "bottom": 1,
            "left": 0,
            "right": 0,
        }

    def check_snap(self, side: str, tile: Tile, check_tile: Tile | JigSaw):
        """Checks if the tile can be snapped to the check_tile or the game border and snaps it if it can"""
        side_axis = self.sides_axes[side]
        # snapping distance is 15% of the tile's either width or height
        snapping_distance = tile.rect.size[side_axis] / 100 * 15

        # border snapping
        if isinstance(check_tile, JigSaw):
            if tile.rect.topleft[side_axis] < snapping_distance:
                # snaps the tile's left side to the left game border
                tile.snap("topleft", 0, side_axis)
                return True
            elif tile.rect.bottomright[side_axis] > (
                self.jigsaw.size[side_axis] - snapping_distance
            ):
                # snaps the tile's right side to the right game border
                tile.snap("bottomright", self.jigsaw.size[side_axis], side_axis)
                return True
        # tile snapping
        else:
            topleft_snap = abs(
                check_tile.rect.bottomright[side_axis] - tile.rect.topleft[side_axis]
            )
            bottomright_snap = abs(
                check_tile.rect.topleft[side_axis] - tile.rect.bottomright[side_axis]
            )
            if topleft_snap < bottomright_snap and topleft_snap <= snapping_distance:
                # snaps the tile's left side to the right side of the check_tile
                tile.snap("topleft", check_tile.rect.bottomright[side_axis], side_axis)
                return True
            elif bottomright_snap <= snapping_distance:
                # snaps the tile's right side to the left side of the check_tile
                tile.snap("bottomright", check_tile.rect.topleft[side_axis], side_axis)
                return True

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
                        if tile.active:
                            h_snapped = self.check_snap("left", tile, self.jigsaw)
                            if not h_snapped:
                                h_snapped = self.check_snap("right", tile, self.jigsaw)
                            v_snapped = self.check_snap("top", tile, self.jigsaw)
                            if not v_snapped:
                                v_snapped = self.check_snap("bottom", tile, self.jigsaw)
                            for check_tile in self.tiles.sprites()[::-1]:
                                if v_snapped and h_snapped:
                                    # if the tile has been snapped on the 2 axis, no need to check the other tiles
                                    break
                                if check_tile != tile:
                                    if not h_snapped:
                                        h_snapped = self.check_snap(
                                            "left", tile, check_tile
                                        )
                                        if not h_snapped:
                                            h_snapped = self.check_snap(
                                                "right", tile, check_tile
                                            )
                                    if not v_snapped:
                                        v_snapped = self.check_snap(
                                            "top", tile, check_tile
                                        )
                                        if not v_snapped:
                                            v_snapped = self.check_snap(
                                                "bottom", tile, check_tile
                                            )
                        tile.deactivate()
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
