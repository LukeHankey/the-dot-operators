#!/usr/bin/venv python3
"""Core Image Manipulation functionality"""

from math import sqrt
from random import shuffle

from PIL.Image import Image, open


def get_image(
    filename: str, max_dimensions: tuple[int, int], num_of_tiles: int
) -> Image:
    """This could be extended to by addeding filters, and from other sources"""
    with open(filename) as image:
        image.thumbnail(max_dimensions)
        num_of_tiles = int(sqrt(num_of_tiles))

        width = image.width // num_of_tiles
        height = image.height // num_of_tiles
        image = image.crop((0, 0, num_of_tiles * width, num_of_tiles * height))

    return image


def tile_scrambler(
    tiles: dict[tuple[int, int], Image]
) -> list[tuple[tuple[int, int], Image]]:
    """Extract out the positions to shuffle then add back in"""
    # extract out the positions to shuffle then add back in
    positions = list(tiles)
    shuffle(positions)
    return zip(positions, tiles.values())
