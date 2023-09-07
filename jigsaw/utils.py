#!/usr/bin/venv python3
"""Core Image Manipulation functionality"""

from collections.abc import Callable, Generator
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


def regular(
    tile_generator: Callable[
        [Image, int, int], Generator[tuple[tuple[int, int], Image], None, None]
    ],
    image: Image,
    num_of_tiles: int,
) -> dict[tuple[int, int], Image]:
    """Opens image file and splits it into tiles and shuffles them"""
    sequence: dict[tuple[int, int], Image] = {}
    num_of_tiles = int(sqrt(num_of_tiles))

    width = image.width // num_of_tiles
    height = image.height // num_of_tiles

    for pos, tile in tile_generator(image, width, height):
        sequence[pos] = tile

    return sequence


def tile_scrambler(
    tiles: dict[tuple[int, int], Image]
) -> list[tuple[tuple[int, int], Image]]:
    """Extract out the positions to shuffle then add back in"""
    # extract out the positions to shuffle then add back in
    positions = list(tiles)
    shuffle(positions)

    new_sequence = [
        (position, image) for position, image in zip(positions, tiles.values())
    ]

    return new_sequence
