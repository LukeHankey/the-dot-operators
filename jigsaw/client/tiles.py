from collections.abc import Generator
from typing import Literal

from PIL.Image import Image, new
from PIL.ImageDraw import Draw
from pygame import image, sprite


class Tile(sprite.Sprite):
    """Tile which is a cropped image at a specifc point.

    dragging support is built in TODO; add support for alpha, better
    bounding box methods
    """

    def __init__(self, pos: tuple[int, int], overlap, cropped_image: Image) -> None:
        """Basic init method that takes pillow image into pygame image"""
        super().__init__()
        self.image = image.fromstring(
            cropped_image.tobytes(), cropped_image.size, cropped_image.mode
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.active = False
        self.drag_offset: tuple[int, int]
        self.snapping_rect = (self.rect.size[0] * overlap, self.rect.size[1] * overlap)

    def activate(self, pointer: tuple[int, int]) -> None:
        """Could add tile highlighting and other affects"""
        self.active = True
        self.drag_offset = (
            pointer[0] - self.rect.topleft[0],
            pointer[1] - self.rect.topleft[1],
        )

    def deactivate(self) -> None:
        """Remove anything `activate` added"""
        self.active = False
        self.drag_offset = (0, 0)  # so move can be used more directly

    def move(self, pointer: tuple[int, int]) -> None:
        """Move tile to pointer could be a mouse pointer or anything"""
        self.rect.topleft = (
            pointer[0] - self.drag_offset[0],
            pointer[1] - self.drag_offset[1],
        )

    def snap(self, side: str, coord: int, axis: int) -> Literal[True]:
        """Snaps the tile to other tiles/image borders on the horizontal axis"""
        if side == "topleft":
            tmp_coord = list(self.rect.topleft)
            tmp_coord[axis] = coord
            self.rect.topleft = tuple(tmp_coord)
        else:
            tmp_coord = list(self.rect.bottomright)
            tmp_coord[axis] = coord
            self.rect.bottomright = tuple(tmp_coord)
        return True


class JigSawTiles(sprite.Group):
    """Inheritance for the addition of Group methods concerning active tiles"""

    def get_active(self) -> Tile | None:
        """Return the active tile"""
        for tile in self.sprites()[::-1]:
            if tile.active:
                return tile
        return None

    def get_inactives(self) -> list[Tile]:
        """Return the inactive tiles"""
        return [tile for tile in self.sprites() if not tile.active]


def trianglular_tiles(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile generator with the inner most loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            mask = new("L", (width, height), 0)
            draw = Draw(mask)
            draw.polygon([(0, 0), (0, height), (width, height)], fill=255)
            tile = image.crop((x, y, x + width, y + height))
            tile.putalpha(mask)
            yield (x, y), tile  # first yield for half the triangle

            mask = new("L", (width, height), 0)
            draw = Draw(mask)
            draw.polygon([(0, 0), (width, 0), (width, height)], fill=255)
            tile = image.crop((x, y, x + width, y + height))
            tile.putalpha(mask)
            yield (x, y), tile  # second yield for the other half


def square_tiles(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile generator with the inner most loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            yield (x, y), image.crop((x, y, x + width, y + height))
