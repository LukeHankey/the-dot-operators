#!/usr/bin/venv python3
"""Core Image Manipulation functionality"""

from math import sqrt
from operator import itemgetter
from random import shuffle
from typing import Callable, Generator

from PIL.Image import Image, new, open
from PIL.ImageDraw import Draw


def triangle_tiles(image: Image, width: int, height: int) -> Generator[[[int, int], Image], None, None]:
    """Tile generator with the inner most loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            mask = new('L', (width, height), 0)
            draw = Draw(mask)
            draw.polygon([(0, 0), (0, height), (width, height)], fill=255)
            tile = image.crop((x, y, x + width, y + height))
            tile.putalpha(mask)
            yield (x, y), tile  # first yeild for half the triangle
            mask = new('L', (width, height), 0)
            draw = Draw(mask)
            draw.polygon([(0, 0), (width, 0), (width, height)], fill=255)
            tile = image.crop((x, y, x + width, y + height))
            tile.putalpha(mask)
            yield (x, y), tile  # second yield for the other half


def square_tiles(image: Image, width: int, height: int) -> Generator[[[int, int], Image], None, None]:
    """Tile generator with the inner most loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            yield (x, y), image.crop((x, y, x + width, y + height))


def regular_tiles(
        filename: str,
        num_tiles: int,
        tile_generator: Callable[[Image, int, int], Generator[[[int, int], Image], None, None]]) -> list:
    """Opens image file and splits it into tiles and shuffles them"""
    with open(filename) as image:
        image.thumbnail((720, 480))
        sequence = list()
        width = int(image.width // sqrt(num_tiles))
        height = int(image.height // sqrt(num_tiles))
        for num, (pos, tile) in enumerate(tile_generator(image, width, height)):
            sequence.append([pos, tile])
    # extract out the positions to shuffle then add back in
    positions = list(map(itemgetter(0), sequence))
    shuffle(positions)
    for index, position in enumerate(positions):
        sequence[index][0] = position
    return sequence


if __name__ == "__main__":
    from os import listdir
    from os.path import join, split
    from random import choice
    path = join(split(__file__)[0], "images")
    filename = choice([  # get a random image on each game run
        f"images/{filename}" for filename in listdir(path)])
    filename = join(split(__file__)[0], filename)
    for _, tile in regular_tiles(filename, 4, triangle_tiles):
        tile.show()
