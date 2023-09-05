from collections.abc import Generator
from math import sqrt
from operator import itemgetter
from random import shuffle
from typing import Callable

from PIL.Image import Image, new
from PIL.ImageDraw import Draw


# See: http://www.cut-the-knot.org/triangle/MidpointsInHexagon.shtml
def tile_splitter(
    tiler: Callable[
        [Image, int, int], Generator[tuple[tuple[int, int], Image], None, None]
    ],
    image: Image,
    num_of_tiles: int,
) -> list:
    """Opens image file and splits it into tiles and shuffles them"""
    sequence = list()
    num_of_tiles = int(sqrt(num_of_tiles))
    width = image.width // num_of_tiles
    height = image.height // num_of_tiles
    for num, (pos, tile_) in enumerate(tiler(image, width, height)):
        sequence.append([pos, tile_])
    # extract out the positions to shuffle then add back in
    positions = list(map(itemgetter(0), sequence))
    shuffle(positions)
    for index, position in enumerate(positions):
        sequence[index][0] = position
    return sequence


def square_tiler(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile generator with the innermost loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            yield (x, y), image.crop((x, y, x + width, y + height))


def triangular_tiler(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile generator with the innermost loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            mask = new("L", (width, height), 0)
            draw = Draw(mask)
            draw.polygon([(0, 0), (0, height), (width, height)], fill=255)
            tile = image.crop((x, y, x + width, y + height))
            tile.putalpha(mask)
            yield (x, y), tile  # first yeild for half the triangle
            mask = new("L", (width, height), 0)
            draw = Draw(mask)
            draw.polygon([(0, 0), (width, 0), (width, height)], fill=255)
            tile = image.crop((x, y, x + width, y + height))
            tile.putalpha(mask)
            yield (x, y), tile  # second yield for the other half


def hexagonal_tiler(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile image into hexagonal tiles."""
    raise NotImplementedError("hexagonal_tiler not yet implemented")


def deltoidal_trihexagonal_tiler(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile image into deltoidal trihexagonal tiles. Deltoidal trihexagonal tiles are hexagons divided into kites."""
    raise NotImplementedError("deltoidal_trihexagonal_tiler not yet implemented")


def einstein_tiler(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """
    Tile image into einstein tiles.

    This is an aperiodic monotile composed of 8 kites from a deltoidal trihexagonal tile.
    """
    raise NotImplementedError("einstein_tiler not yet implemented")
