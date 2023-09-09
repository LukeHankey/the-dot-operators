#!/usr/bin/venv python3
"""Core Image Manipulation functionality"""

from collections.abc import Generator
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
    tiles: Generator[tuple[tuple[int, int], Image], None, None]
) -> list[tuple[tuple[int, int], Image]]:
    """Extract out the positions to shuffle then add back in"""
    # extract out the positions to shuffle then add back in
    gen_list = list(tiles)
    positions = [pos for pos, _ in gen_list]
    tile_list = [tile for _, tile in gen_list]
    shuffle(positions)
    return zip(positions, tile_list)
